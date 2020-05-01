"""WiLight Protocol Support."""
import asyncio
from collections import deque
import logging
import codecs
import binascii


class WiLightProtocol(asyncio.Protocol):
    """WiLight device control protocol."""

    transport = None  # type: asyncio.Transport

    def __init__(self, client, disconnect_callback=None, loop=None,
                 logger=None):
        """Initialize the WiLight protocol."""
        self.client = client
        self.loop = loop
        self.logger = logger
        self._buffer = b''
        self.disconnect_callback = disconnect_callback
        self._timeout = None
        self._cmd_timeout = None
        self._keep_alive = None

    def connection_made(self, transport):
        """Initialize protocol transport."""
        self.transport = transport
        self._reset_timeout()

    def _send_keepalive_packet(self):
        """Send a keep alive packet."""
        if not self.client.in_transaction:
            packet = self.format_packet("000000", self.client.num_serial)
            #self.logger.warning('sending packet keep alive: %s', packet)
            self.logger.debug('sending keep alive packet')
            self.transport.write(packet)

    def _reset_timeout(self):
        """Reset timeout for date keep alive."""
        if self._timeout:
            self._timeout.cancel()
        self._timeout = self.loop.call_later(self.client.timeout,
                                             self.transport.close)
        if self._keep_alive:
            self._keep_alive.cancel()
        self._keep_alive = self.loop.call_later(
            self.client.keep_alive_interval,
            self._send_keepalive_packet)

    def reset_cmd_timeout(self):
        """Reset timeout for command execution."""
        if self._cmd_timeout:
            self._cmd_timeout.cancel()
        self._cmd_timeout = self.loop.call_later(self.client.timeout,
                                                 self.transport.close)

    def data_received(self, data):
        """Add incoming data to buffer."""
#        self._buffer += data
        self._buffer = data
        #self.logger.warning('recebeu data: %s', self._buffer)
        self._handle_lines()

    def _handle_lines(self):
        """Assemble incoming data into per-line packets."""
        if b'&' in self._buffer:
            line = self._buffer[0:len(self._buffer)]
            if self._valid_packet(self, line):
                #self.logger.warning('recebeu data valida')
                self._handle_packet(line)
            else:
                self.logger.warning('dropping invalid data: %s', line)

    @staticmethod
    def _valid_packet(self, packet):
        """Validate incoming packet."""
        if packet[0:1] != b'&':
            return False
#        self.logger.warning('len %i', len(packet))
        if len(packet) < 60:
            return False
        b_num_serial = self.client.num_serial.encode()
        #self.logger.warning('b_num_serial %s', b_num_serial)
        for i in range(0, 12):
            if packet[i + 1] != b_num_serial[i]:
                return False
        return True

    def _handle_packet(self, packet):
        """Parse incoming packet."""
        #self.logger.warning('handle data: %s', packet)
        if packet[0:1] == b'&':
            if self.client.model == "0102":
                self._handle_0102_packet(packet)
        else:
            self.logger.warning('received unknown packet: %s', packet)

    def _handle_0102_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 3):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            self.logger.warning('estado index %i: %s', index, on)
            states[format(index, 'x')] = {"on": on}
            mudou = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    mudou = True
            else:
                mudou = True
            if mudou:
                changes.append(format(index, 'x'))
                self.client.states[format(index, 'x')] = {"on": on}

        for index in changes:
            for status_cb in self.client.status_callbacks.get(index, []):
                status_cb(states[index])
        self.logger.debug(states)
        if self.client.in_transaction:
            self.client.in_transaction = False
            self.client.active_packet = None
            self.client.active_transaction.set_result(states)
            while self.client.status_waiters:
                waiter = self.client.status_waiters.popleft()
                waiter.set_result(states)
            if self.client.waiters:
                self.send_packet()
            else:
                self._cmd_timeout.cancel()
        elif self._cmd_timeout:
            self._cmd_timeout.cancel()

    def send_packet(self):
        """Write next packet in send queue."""
        waiter, packet = self.client.waiters.popleft()
        #self.logger.warning('sending packet send_packet: %s', packet)
        self.client.active_transaction = waiter
        self.client.in_transaction = True
        self.client.active_packet = packet
        self.reset_cmd_timeout()
        self.transport.write(packet)

    @staticmethod
    def format_packet(command, num_serial):
        """Format packet to be sent."""
        frame_header = b"!" + num_serial.encode()
        return frame_header + command.encode()

    def connection_lost(self, exc):
        """Log when connection is closed, if needed call callback."""
        if exc:
            self.logger.error('disconnected due to error')
        else:
            self.logger.info('disconnected because of close/abort.')
        if self._keep_alive:
            self._keep_alive.cancel()
        if self.disconnect_callback:
            asyncio.ensure_future(self.disconnect_callback(), loop=self.loop)


class WiLightClient:
    """WiLight client wrapper class."""

    def __init__(self, device_id, host, port, model, config_ex,
                 disconnect_callback=None, reconnect_callback=None,
                 loop=None, logger=None, timeout=10, reconnect_interval=10,
                 keep_alive_interval=3):
        """Initialize the WiLight client wrapper."""
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
        self.num_serial = device_id[2:]
        self.device_id = device_id
        self.host = host
        self.port = port
        self.model = model
        self.config_ex = config_ex
        self.transport = None
        self.protocol = None
        self.is_connected = False
        self.reconnect = True
        self.timeout = timeout
        self.reconnect_interval = reconnect_interval
        self.keep_alive_interval = keep_alive_interval
        self.disconnect_callback = disconnect_callback
        self.reconnect_callback = reconnect_callback
        self.waiters = deque()
        self.status_waiters = deque()
        self.in_transaction = False
        self.active_transaction = None
        self.active_packet = None
        self.status_callbacks = {}
        self.states = {}

    async def setup(self):
        """Set up the connection with automatic retry."""
        while True:
            fut = self.loop.create_connection(
                lambda: WiLightProtocol(
                    self,
                    disconnect_callback=self.handle_disconnect_callback,
                    loop=self.loop, logger=self.logger),
                host=self.host,
                port=self.port)
            try:
                self.transport, self.protocol = \
                    await asyncio.wait_for(fut, timeout=self.timeout)
            except asyncio.TimeoutError:
                self.logger.warning("Could not connect due to timeout error.")
            except OSError as exc:
                self.logger.warning("Could not connect due to error: %s",
                                    str(exc))
            else:
                self.is_connected = True
                if self.reconnect_callback:
                    self.reconnect_callback()
                break
            await asyncio.sleep(self.reconnect_interval)

    def stop(self):
        """Shut down transport."""
        self.reconnect = False
        self.logger.debug("Shutting down.")
        if self.transport:
            self.transport.close()

    async def handle_disconnect_callback(self):
        """Reconnect automatically unless stopping."""
        self.is_connected = False
        if self.disconnect_callback:
            self.disconnect_callback()
        if self.reconnect:
            self.logger.debug("Protocol disconnected...reconnecting")
            await self.setup()
            self.protocol.reset_cmd_timeout()
            if self.in_transaction:
                self.protocol.transport.write(self.active_packet)
            else:
                packet = self.protocol.format_packet("000000", self.num_serial)
                #self.logger.warning('sending packet disconnected: %s', packet)
                self.protocol.transport.write(packet)

    def register_status_callback(self, callback, index):
        """Register a callback which will fire when state changes."""
        if self.status_callbacks.get(index, None) is None:
            self.status_callbacks[index] = []
        self.status_callbacks[index].append(callback)

    def _send(self, packet):
        """Add packet to send queue."""
        #self.logger.warning('sending packet _send: %s', packet)
        fut = self.loop.create_future()
        self.waiters.append((fut, packet))
        if self.waiters and self.in_transaction is False:
            self.protocol.send_packet()
        return fut

    async def turn_on(self, index=None):
        """Turn on relay."""
        if index is not None:
            #self.logger.warning('index turn_on ok: %s', index)
            comandos_on = ["001000", "003000", "005000"]
            packet = self.protocol.format_packet(comandos_on[int(index)], self.num_serial)
        else:
            #self.logger.warning('index turn_on nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        states = await self._send(packet)
        return states

    async def turn_off(self, index=None):
        """Turn off relay."""
        if index is not None:
            #self.logger.warning('index turn_off ok: %s', index)
            comandos_off = ["002000", "004000", "006000"]
            packet = self.protocol.format_packet(comandos_off[int(index)], self.num_serial)
        else:
            #self.logger.warning('index turn_off nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        states = await self._send(packet)
        return states

    async def status(self, index=None):
        """Get current relay status."""
        if index is not None:
            if self.waiters or self.in_transaction:
                fut = self.loop.create_future()
                self.status_waiters.append(fut)
                states = await fut
                state = states[index]
            else:
                packet = self.protocol.format_packet("000000", self.num_serial)
                self.logger.warning('sending packet status 1: %s', packet)
                states = await self._send(packet)
                state = states[index]
        else:
            if self.waiters or self.in_transaction:
                fut = self.loop.create_future()
                self.status_waiters.append(fut)
                state = await fut
            else:
                packet = self.protocol.format_packet("000000", self.num_serial)
                self.logger.warning('sending packet status 1: %s', packet)
                state = await self._send(packet)
        return state


async def create_wilight_connection(device_id=None,
                                     host=None,
                                     port=None,
                                     model=None,
                                     config_ex=None,
                                     disconnect_callback=None,
                                     reconnect_callback=None, loop=None,
                                     logger=None, timeout=None,
                                     reconnect_interval=None,
                                     keep_alive_interval=None):
    """Create WiLight Client class."""
    client = WiLightClient(device_id=device_id, host=host, port=port, model=model, config_ex=config_ex,
                        disconnect_callback=disconnect_callback,
                        reconnect_callback=reconnect_callback,
                        loop=loop, logger=logger,
                        timeout=timeout, reconnect_interval=reconnect_interval,
                        keep_alive_interval=keep_alive_interval)
    await client.setup()

    return client
