""" Server/client communication via TCP sockets.
The module implements TCP communication between
a daemon-like :class:`Server` and a simple
:class:`Client`.

The :class:`Server` class is meant to be
run by a daemon-like app. The user should
override the :meth:`~Server.task` method which
defines the server behaviour upon reception
of a message from the :class:`Client`.

The :class:`Client` class communicates with
the server and sends commands to this
user-defined function. The special command
'quit' will terminate the :class:`Server`.

The module is based upon `this tutorial
<https://pymotw.com/2/socket/tcp.html>`_.

Attributes
----------
buffer_size: int, 1024
    Maximum length of a transmitted messages
"""

import socket
import configparser
import logging
from pkg_resources import resource_filename
from zc.lockfile import LockFile, LockError

# Maximum length of transmitted messages
buffer_size: int = 1024


class Server:
    """ Simple TCP Server. The server is meant to
    be run by a daemon-like app. The user should
    override the :meth:`~Server.task` method, which
    defines the server behaviour upon reception
    of a message from the :class:`Client`.
    """

    # Attributes
    host: str = 'localhost'         #: Host address.
    port: int = 1507                #: Connection port.
    sock: socket.SocketType = None  #: Connection socket.
    logger: logging.Logger = None   #: Single logger for the whole class.
    message: str = ''               #: Message from the client.
    reply: str = ''                 #: Reply to the client.
    max_backlog: int = 1            #: TCP connection queue.
    lock: LockFile = None           #: Lock file to become a daemon

    def __init__(self, config_file: str = None):
        """ Initializes the :class:`Server` object. The
        constructor calls the :meth:`config` method to
        read out the server attributes.

        Parameters
        ----------
        config_file : str, optional
            Configuration file, default is `None`.

        Raises
        ------
        :class:`configparser.Error`
           A configuration file is given but the method
            :meth:`config` fails
        """

        # Read config file
        if config_file is not None:
            self.config(config_file)

        # Use a single logger for all server messages
        self.logger = logging.getLogger('Server on {h}:{p}'.format(h=self.host, p=self.port))

    def __del__(self):
        """ Releases the PID lock file. """
        if self.lock is not None:
            self.logger.info('Releasing PID file')
            self.lock.close()

    def daemonize(self, pid_file_name: str):
        """ Locks a PID file to ensure a single instance of the
        server is running.

        Parameters
        ----------
        pid_file_name : str
            PID file name to lock.

        Raises
        ------
        :class:`LockError`
           The PID file could not be locked.
        """
        try:
            self.logger.info('Locking PID file {f}'.format(f=pid_file_name))
            self.lock = LockFile(
                path=pid_file_name,
                content_template='{pid};{hostname}'
            )
        except LockError as e:
            self.logger.error("{}: {}".format(type(e).__name__, e))
            raise

    def config(self, filename: str):
        """ Loads the server configuration from a file.

        Parameters
        ----------
        filename : str
            The file name to be read.

        Raises
        ------
        :class:`configparser.Error`
            If an error happened while parsing the file, e.g. no file was found
        """

        # Use a logger named like the module itself
        logger = logging.getLogger(__name__)
        logger.info("Loading configuration file %s", filename)

        try:
            # Initialize config parser and read file
            config_parser = configparser.ConfigParser()
            config_parser.read(filename)

            # Assign values to class attributes
            self.host = config_parser.get(section='Overall', option='host', fallback='localhost')
            self.port = config_parser.getint(section='Overall', option='port', fallback=1507)

        except configparser.Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def start(self):
        """ Starts the server.
        The server will run in an endless loop
        until the message 'quit' is received.

        Raises
        ------
        :class:`OSError`
            Various socket errors, e.g. address or timeout
        """

        try:
            # Bind the server to the address
            self.logger.info('Binding to address {h}:{p}'.format(h=self.host, p=self.port))
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(self.max_backlog)
            self.logger.info('Server is now listening, send a \'quit\' message to stop it')
            while True:
                # Accept connection
                connection, client_address = self.sock.accept()
                try:
                    # Receive message
                    self.logger.info('Client connected from %s', client_address)
                    self.message = connection.recv(buffer_size).decode().rstrip()
                    self.logger.info('Message: %s', self.message)

                    # Call server task
                    self.task()

                    # Send reply to client
                    self.logger.info('Sending reply: %s', self.reply)
                    # TODO: check that len(self.reply) < buffer_size
                    connection.sendall(self.reply.encode())

                except OSError as e:
                    self.logger.error("{}: {}".format(type(e).__name__, e))
                    self.logger.error("Server could recover and is still listening")

                finally:
                    # Close connection
                    self.logger.info('Closing connection to client %s', client_address)
                    connection.close()

                # Quit?
                if self.message == 'quit':
                    self.logger.info('Quitting now...')
                    break

        except OSError as e:
            self.logger.error("{}: {}".format(type(e).__name__, e))
            raise

    def stop(self):
        c = Client(
            host=self.host,
            port=self.port,
        )
        c.send_message('quit')

    def status(self) -> str:
        c = Client(
            host=self.host,
            port=self.port,
        )

        return c.send_message('status')

    def task(self):
        """Server task, called upon reception of a
        message from a :obj:`client<Client>`.

        The default task is a simple echo that
        assigns the :attr:`message` received to
        the :attr:`reply`. Users should
        override this method with their own
        task for their custom application.

        If the :attr:`message` received is 'quit',
        the TCP server will stop after this last
        task is performed, so the users should do
        proper clean-up in this last operation.

        The task should always set the attribute
        :attr:`reply`, which will be sent back
        to the :obj:`client<Client>`.
        """
        self.reply = self.message


class Client:
    """ Simple TCP client to communicate with a
    running :class:`Server`. It sends a
    message and receives the reply from the
    server.
    """

    # Attributes
    host: str = 'localhost'     #: Host address.
    port: int = 1507            #: Connection port.

    def __init__(self, config_file: str = None, host: str = None, port: int = None):
        """ Initializes the :class:`Client` object. If a
        :paramref:`~Client.__init__.config_file`
        is given, the constructor calls the
        :meth:`~.Client.config` method and
        overrides the default attributes. If the
        parameters :paramref:`host` and
        :paramref:`port` are given, they will
        override the configuration file.

        Parameters
        ----------
        config_file : str, optional
            Configuration file name, default is `None`. Same as
            See the example TODO.

        host : str, optional
            Host address, default is `None`.

        port : int, optional
            Connection port, default is `None`.


        Raises
        ------
        :class:`configparser.Error`
            If a configuration file name was given, the method
            :meth:`config` can fail raising this exception.
        """

        # Read config file, if given
        if config_file is not None:
            self.config(config_file)

        # Override attributes, if given
        if host is not None:
            self.host = host

        if port is not None:
            self.port = port

    def config(self, config_file: str = resource_filename(__name__, 'conf/server.ini')):
        """ Loads the configuration from a file.

        The method reads the :paramref:`config_file`
        using the library :obj:`configparser`. The
        structure of the file is shown in the
        :ref:`examples section<configuration-files>`.

        Parameters
        ----------
        config_file : str, optional
            TODO

        Raises
        ------
        :class:`configparser.Error`
            Error while parsing the file, e.g. no file was found,
            a parameter is missing or it has an invalid value.
        """

        # Use a logger named like the module itself
        logger = logging.getLogger(__name__)
        logger.info("Loading configuration file %s", config_file)

        try:
            # Initialize config parser and read file
            config_parser = configparser.ConfigParser()
            config_parser.read(config_file)

            # Assign values to class attributes
            self.host = config_parser.get(section='Overall', option='host', fallback='localhost')
            self.port = config_parser.getint(section='Overall', option='port', fallback=1507)

        except configparser.Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

        else:
            logger.info("Configuration file loaded")

    def send_message(self, msg: str) -> str:
        """ Complete communication process. Connects
        to the server, sends a message, gets the reply
        and closes the connection.

        Raises
        ------
        :class:`OSError`
            Various socket errors, e.g. address or timeout

        Returns
        -------
        str
            Reply from the server
        """

        # Get the logger
        logger = logging.getLogger(__name__)
        logger.info('Sending message to the server: %s', msg)

        try:
            # Connect to the server
            sock = socket.create_connection((self.host, self.port))

            # Send message
            # TODO: check message length
            sock.sendall(msg.encode())

            # Get reply
            reply = sock.recv(buffer_size).decode()
            logger.info('Reply received: %s', reply)

            # Close the connection
            sock.close()

        except OSError as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

        else:
            return repr(reply)
