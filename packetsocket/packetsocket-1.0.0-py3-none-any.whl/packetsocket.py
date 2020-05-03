#!/usr/bin/env python3

"""High-level socket interface for non-blocking packet communication.

packetsocket provides a simple, high-level class interface for non-blocking
sockets communicating in packet messages. Two types of sockets
are implemented: `PacketSocketServer` and `PacketSocketClient`. A server can accept incoming
client connections, a client can connect to one server. Both inherit the common PacketSocket
operations (`open`, `close`, `update`, `read`, `write`) from the base class `PacketSocket`.
These methods are thread-safe using an internal lock.

PacketSockets work in non-blocking mode regarding the sending and receiving of socket messages.
They do, however, have the option to block while waiting for the lock.

PacketSockets communicate messages as simple packets. They are composed as follows:
"<HEADER_PREFIX><body-size><body>"
where <HEADER_PREFIX> is the constant bytestring `PacketSocket.HEADER_PREFIX` identifying the
beginning of a new message, <body-size> stores the size of the body of a fixed length of
`PacketSocket.HEADER_BYTES` bytes, and <body> is the message itself.


Example of Server - Client communication::

    from queue import Queue
    from threading import Thread

    from packetsocket import PacketSocketServer, PacketSocketClient

    ADDRESS = ("", 4200)
    messages = Queue()
    running = True


    def runServer(messages, address, running):
        with PacketSocketServer(address) as server:
            while running:
                while not messages.empty():
                    msg = messages.get_nowait()
                    server.write(msg)

                server.update()

                for sock, msgs in server.read():
                    client_name = sock.getpeername()[0]
                    for msg in msgs:
                        print(f"[{client_name}] {msg.decode()}")


    def runClient(messages, address, running):
        with PacketSocketClient(ADDRESS) as client:
            while running:
                client.update()

                for msg in client.read():
                    print(f"[Server] {msg.decode()}")
                    client.write(b"<Server Echo> " + msg)


    def getInput(messages, running):
        while running:
            inp = input("Send message to client: \n")
            if inp.strip():
                messages.put(inp.encode())
                print("\n")


    try:
        Thread(target=getInput, args=(messages, running)).start()
        Thread(target=runServer, args=(messages, ADDRESS, running)).start()
        Thread(target=runClient, args=(messages, ADDRESS, running)).start()
    finally:
        running = False
"""


import socket
import socket as _socket
import select
import logging
from threading import RLock
from collections import deque
from contextlib import contextmanager


__author__ = "Kevin Hambrecht"
__copyright__ = "I don't do copyrights"
__credits__ = []
__license__ = "Neither do I do these"
__version__ = "1.0.0"
__maintainer__ = "Kevin Hambrecht"
__email__ = "kev.hambrecht@gmail.com"
__status__ = "Prototype"


@contextmanager
def blockableLock(lock, blocking=True):
    """Helper contextmanager for blockable locks.

    Args:
        lock (threading.[R]Lock): Lock object.
        blocking (bool): Acquire lock in blocking mode. Defaults to `True`.

    Returns:
        threading.[R]Lock | `False`: Returns the lock object or `False`
            if lock could not be acquired in non-blocking mode.

    Examples:
        Use the blockableLock context like this::

            my_lock = threading.Lock()
            with blockableLock(my_lock, blocking=False) as lock:
                if lock:    # Lock acquired
                    doStuff()
    """
    if lock.acquire(blocking=blocking):
        try:
            yield lock
        finally:
            lock.release()
    else:
        yield False



class PacketSocket(object):
    """Base class for non-blocking, headered sockets.

    Attributes:
        address (tuple): Tuple of (<host>, <port>).
        socket (socket.socket): socket object.
        socket_buffer (dict): Dictionary storing the read and write buffer as `collection.deque`s
            for every active socket::

                {<socket> : [<read-buffer-deque>, <write-buffer-deque>]}

        lock (`threading.RLock`): RLock object.

        HEADER_PREFIX (bytearray): Header prefix to identify the start of an incoming packet
        HEADER_BYTES (int): Length of header in bytes, excluding the `HEADER_PREFIX`.
        RECV_BUFSIZE (int): Buffersize in bytes for `socket.recv`.
        SELECT_TIMEOUT_S (float): Timeout in seconds for `select.select`.

    Notes:
        `PacketSocket`s supports the context management protocol::

            with PacketSocket(blocking=False) as sock:
                if not sock:    # Check for success for non-blocking requests
                    print("Could not open socket, busy. Try again.")
                else:
                    print("Socket opened")

        The `blocking` parameters refer to the lock object, NOT the socket. Socket operations
        are always performed non-blocking.

        All public functions (`open`, `close`, `update`, `read`, `write`) are a thread-safe wrapper of
        the corresponding private functions (`_open`, ...), which are to be implemented by subclasses.
    """

    def __init__(self, address, *args, blocking=True, **kwargs):
        """
        Args:
            address (tuple): Socket address tuple of (<host>, <port>).
            blocking (bool): Blocking mode for entering the context manager. Defaults to `True`.
        """
        self.address = address
        self.socket = None
        self.sockets_buffer = {}
        self.lock = RLock()
        self._enter_blocking = blocking

        self.HEADER_PREFIX = b"#!?&"
        self.HEADER_BYTES = 4
        self.RECV_BUFSIZE = 2**17
        self.SELECT_TIMEOUT_S = 0.005



    def __enter__(self):
        if self.open(self._enter_blocking) is False:
            return False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



    @property
    def active_socket_count(self):
        """int: Number of active sockets."""
        return len(self.sockets_buffer)

    @property
    def is_open(self):
        """bool: Is the socket open."""
        return (self.socket is not None)



    def assertOpenSocket(self):
        """Assert that the socket is open.

        Raises:
            IOError: If assertion fails.
        """
        if not self.is_open:
            raise IOError("Socket not open")


    def open(self, *args, blocking=True, **kwargs):
        """Open the socket."""
        with blockableLock(self.lock, blocking=blocking) as lock:
            if not lock:
                return False
            logging.info("Opening socket")
            return self._open(*args, **kwargs)

    def close(self, *args, blocking=True, **kwargs):
        """Close the socket and its connections."""
        with blockableLock(self.lock, blocking=blocking) as lock:
            if not lock:
                return False
            logging.info("Closing socket")
            return self._close(*args, **kwargs)

    def update(self, *args, blocking=False, **kwargs):
        """Perform read and write actions.

        This method performs the actual non-blocking socket actions, reading incoming messages
        into the respective reading buffer and writing the messages from the writing buffer to
        the respective sockets. This should best be called continuously, with little delay, ideally
        before `read` and after `write`.
        """
        with blockableLock(self.lock, blocking=blocking) as lock:
            if not lock:
                return False
            self.assertOpenSocket()
            return self._update(*args, **kwargs)

    def read(self, *args, blocking=False, **kwargs):
        """Read non-empty message queues of all connected sockets."""
        with blockableLock(self.lock, blocking=blocking) as lock:
            if not lock:
                return False
            self.assertOpenSocket()
            return self._read(*args, **kwargs)

    def write(self, *args, blocking=False, **kwargs):
        """Write a message to a socket."""
        with blockableLock(self.lock, blocking=blocking) as lock:
            if not lock:
                return False
            self.assertOpenSocket()
            return self._write(*args, **kwargs)



    def _open(self, *args, blocking=False, **kwargs):
        """Closes the socket if still open and sets up a basic `socket.socket` in non-blocking mode.

        To be implemented/ extended by subclass.
        Don't call this method directly, but use its corresponding thread-safe `write` method.
        """
        if self.is_open:
            self.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)

    def _close(self, *args, blocking=False, **kwargs):
        """Closes the socket if open, resets instance data, and tries to close every connected socket.

        To be implemented/ extended by subclass.
        Don't call this method directly, but use its corresponding thread-safe `write` method.
        """
        if not self.is_open:
            return False

        for sock in list(self.sockets_buffer.keys()):
            self._removeSocket(sock)

        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.socket.close()
        self.socket = None
        self._resetData()

    def _update(self, *args, **kwargs):
        """To be implemented/ extended by subclass.
        Don't call this method directly, but use its corresponding thread-safe `write` method.
        """
        pass

    def _read(self, *args, **kwargs):
        """To be implemented/ extended by subclass.
        Don't call this method directly, but use its corresponding thread-safe `write` method.
        """
        pass

    def _write(self, *args, **kwargs):
        """To be implemented/ extended by subclass.
        Don't call this method directly, but use its corresponding thread-safe `write` method.
        """
        pass


    def _pushMessageToBuffer(self, socket, msg):
        """Push a message to the socket buffer.

        This method creates a packet by prefixing the message with `HEADER_PREFIX`
        and the message length of `HEADER_BYTES` bytes, then pushes it onto the socket's
        writable buffer list.
        """
        header = len(msg).to_bytes(self.HEADER_BYTES, byteorder="little")
        self.sockets_buffer[socket][1].append(self.HEADER_PREFIX + header + msg)


    def _pullMessageFromBuffer(self, socket):
        """Pull the next complete message packet from the socket's buffer.

        Args:
            socket (socket.socket): socket object.

        This method checks the socket's reading buffer queue for the next available, complete
        message packet. If one exists, it is pulled from the queue and its message body is returned.
        Broken packets are discarded.

        Returns:
            bytearray | `False`: Returns the message body if a complete packet is available,
                `False` otherwise.
        """
        buffer_queue = self.sockets_buffer[socket][0]
        buffer_queue_len = len(buffer_queue)

        if buffer_queue_len == 0:
            return False

        if self._calcRemainingPacketSize(buffer_queue[0]) != 0:
            if buffer_queue_len > 1:
                buffer_queue.popleft() # Broken packet
            return False

        buffer = buffer_queue.popleft()
        body = buffer[self.HEADER_BYTES:]
        return body

    def _pullMessagesFromBuffer(self, socket):
        """Pulls all complete packets from the socket's buffer.

        Args:
            socket (socket.socket): socket object.

        Returns:
            list: list of message packets returned from `_pullMessageFromBuffer`.
        """
        messages = []
        while True:
            msg = self._pullMessageFromBuffer(socket)
            if msg is False:
                break
            messages.append(msg)
        return messages

    def _calcRemainingPacketSize(self, packet):
        """Calculate the remaining size of (part of) a packet.

        Uses the header of a packet to determine the complete packet size.

        Args:
            packet (bytearray): Packet buffer
        Returns:
            int: Remaining packet size. May be negative if packet is bigger than its header-defined size.
        """
        body_len = int.from_bytes(packet[:self.HEADER_BYTES], byteorder="little")
        return body_len - len(packet[self.HEADER_BYTES:])


    def _sendBuffer(self, socket):
        """Send the next message of a socket's write buffer.

        Pulls and sends the next message buffer of a socket's write buffer to the socket.
        If zero bytes were sent, an EOF is assumed and handled in `_reachedEOF`.
        The beginning of a socket's write message buffer is guaranteed to algo be the beginning
        of a sent message in order to easily analise a message's header when receiving.

        Args:
            socket (socket.socket): socket object.

        Returns:
            int: Length of sent message in bytes.

        """
        msg = self.sockets_buffer[socket][1].popleft()
        sent_bytes = socket.send(msg)

        if sent_bytes == 0:
            self._reachedEOF()

        msg_left = msg[sent_bytes:]
        if msg_left:
            self.sockets_buffer[socket][1].appendleft(msg_left)
        return sent_bytes


    def _readIntoBuffer(self, socket):
        """Read a socket's incoming message into its buffer.

        Receive and read a socket's incoming message into the socket's write buffer.
        If zero bytes were sent, an EOF is assumed and handled in `_reachedEOF`.
        Every message is checked for being a header and appended to the socket's
        read buffer accordingly.

        Args:
            socket (socket.socket): socket to receive data from.

        Returns:
            int: Length of received message in bytes.
        """

        msg = socket.recv(self.RECV_BUFSIZE)
        msg_len = len(msg)

        if msg_len == 0:
            self._reachedEOF()

        if msg.startswith(self.HEADER_PREFIX):
            msg = msg[len(self.HEADER_PREFIX):]
            self.sockets_buffer[socket][0].append(b"")

        #try:
        self.sockets_buffer[socket][0][-1] += msg
        #except IndexError:
        #    return False

        return msg_len


    def _addSocket(self, socket):
        """Add a newly connected socket."""
        logging.info("Added socket")
        self.sockets_buffer[socket] = [deque(), deque()]

    def _removeSocket(self, socket):
        """Remove and close a connected socket."""
        logging.info("Removing socket")
        try:
            del self.sockets_buffer[socket]
        except KeyError:
            pass
        try:
            socket.shutdown(_socket.SHUT_RDWR)
        except OSError:
            pass
        socket.close()

    def _resetData(self):
        """Reset instance data."""
        self.sockets_buffer.clear()

    def _reachedEOF(self):
        """Handles EOF Exceptions."""
        raise EOFError("Reached end of file.")



class PacketSocketServer(PacketSocket):
    """Non-blocking, headered socket server.

    Attributes:
        MAX_UNACCEPTED_CONNECTIONS (int): Maximum unaccepted connections for socket.listen.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MAX_UNACCEPTED_CONNECTIONS = 0


    def _open(self, *args, **kwargs):
        super()._open(*args, **kwargs)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.socket.listen(self.MAX_UNACCEPTED_CONNECTIONS)


    def _write(self, message, *args, sockets=(), **kwargs):
        """Write a message to a collection of connected sockets.

        Args:
            message (bytearray): Message.
            sockets (tuple): Collection of connected sockets. Defaults to an empty collection,
                sending it to all connected sockets.
        """
        if not sockets:
            sockets = self.sockets_buffer.keys()
        for sock in sockets:
            self._pushMessageToBuffer(sock, message)

    def _read(self, *args, **kwargs):
        """Read non-empty message queues of all connected sockets.

        Yields:
            tuple: Tuple of (<socket>, <msg list>).
        """
        for sock in self.sockets_buffer.keys():
            messages = self._pullMessagesFromBuffer(sock)
            if messages:
                yield (sock, messages)


    def _update(self, *args, **kwargs):
        _rdbl = [self.socket]
        _wtbl = []
        for sock, (r_buffer, w_buffer) in self.sockets_buffer.items():
            _rdbl.append(sock)
            if w_buffer:
                _wtbl.append(sock)

        readable, writable, exceptional = select.select(_rdbl, _wtbl, _rdbl, self.SELECT_TIMEOUT_S)

        for r_socket in readable:
            try:
                if r_socket is self.socket:
                    self._acceptIncomingSocket()
                else:
                    self._readIntoBuffer(r_socket)
            except (BrokenPipeError, ConnectionResetError, EOFError) as e:
                self._removeSocket(r_socket)

        for w_socket in writable:
            try:
                self._sendBuffer(w_socket)
            except (BrokenPipeError, ConnectionResetError, EOFError) as e:
                self._removeSocket(w_socket)

        for err_socket in exceptional:
            self._removeSocket(err_socket)


    def _acceptIncomingSocket(self):
        """Accept and add an incoming sockket connection."""
        logging.info("Accepting incoming connection")
        connection, client_address = self.socket.accept()
        connection.setblocking(False)
        self._addSocket(connection)



class PacketSocketClient(PacketSocket):
    """Non-blocking, headered socket client."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_connected = False


    @property
    def is_connected(self):
        """bool: Is socket connected to server."""
        return self._is_connected


    def _write(self, message, *args, **kwargs):
        """Write message to the server socket.

        Args:
            message (bytearray): Message.
        """
        self._pushMessageToBuffer(self.socket, message)

    def _read(self, *args, **kwargs):
        """Read messages from the server.

        Returns:
            list: Server messages.
        """
        return self._pullMessagesFromBuffer(self.socket)

    def _open(self, *args, **kwargs):
        super()._open(*args, **kwargs)
        self._addSocket(self.socket)

    def _update(self, *args, **kwargs):
        if not self._connect():
            return False

        _s = [self.socket]
        _w = [self.socket] if self.sockets_buffer[self.socket][1] else []
        readable, writable, exceptional = select.select(_s, _w, _s, self.SELECT_TIMEOUT_S)

        if len(readable) > 0:
            data_len = self._readIntoBuffer(self.socket)
            if data_len == 0:
                self.close()

        if len(writable) > 0:
            self._sendBuffer(self.socket)

        if len(exceptional) > 0:
            self.close()


    def _connect(self):
        """Try to connect to the server socket.

        Returns:
            bool: Has successfully connected to the server socket.
        """
        if self.is_connected:
            return True

        _, writable, exceptional = select.select([], [self.socket], [self.socket], self.SELECT_TIMEOUT_S)
        if len(exceptional) > 0:
            return False
        if len(writable) > 0:
            try:
                self.socket.connect(self.address)
            except BlockingIOError:
                return False
            self._is_connected = True
            return True

        return False


    def _resetData(self):
        super()._resetData()
        self._is_connected = False
