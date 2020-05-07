""" Daemon TCP server.
"""

# Imports
from serial.serialutil import SerialException

# Third party
from lab_utils.socket_comm import Server
from lab_utils.database import Database

# Local
from .TPG_256A import TPG_256A
from .__project__ import (
    __documentation__ as docs_url,
    __description__ as prog_desc,
    __module_name__ as mod_name,
)


class Monitor(Server):
    """ Base class of the daemon. It is a child class of
    :class:`~lab_utils.socket_comm.Server`. """

    # Attributes
    handle: TPG_256A = None                 #: Device handle.
    db: Database = None                     #: Database connection.
    use_db: bool = False                    #: Database usage flag.

    def __init__(self,
                 config_file: str = None,
                 pid_file: str = None):
        """ Initializes the :class:`Monitor` object. See
        the documentation of its parent class
        :class:`~lab_utils.socket_comm.Server` for more
        information.
        """
        # Call the parent class initializer
        super().__init__(config_file, pid_file)

        # Add custom arguments to the message parser
        self.update_parser()

        # Initialize database and device handle
        self.handle = TPG_256A()
        # self.db = Database()

    def update_parser(self):
        # Set some properties of the base class argument parser
        self.parser.prog = mod_name
        self.parser.description = prog_desc
        self.parser.epilog = 'Check out the package documentation for more information:\n{}'.format(docs_url)

        # Subparsers for each acceptable command
        # 1. STATUS
        sp_status = self.sp.add_parser(
            name='status',
            description='checks the status of the daemon',
        )
        sp_status.set_defaults(
            func=self.status,
            which='status')

        # 2. TPG-256A
        sp_tpg_256a = self.sp.add_parser(
            name='tpg_256a',
            description='interface to the Pfeiffer TPG 256A',
        )
        sp_tpg_256a.set_defaults(
            func=self.tpg_256a,
            which='tpg_256a'
        )
        sp_g1 = sp_tpg_256a.add_mutually_exclusive_group()
        sp_g1.add_argument(
            '--on',
            action='store_true',
            help='opens the connection to the device',
            default=False,
            dest='turn_on',
        )
        sp_g1.add_argument(
            '--off',
            action='store_true',
            help='closes the connection ',
            default=False,
            dest='turn_off',
        )
        sp_g1.add_argument(
            '--restart',
            action='store_true',
            help='restarts the connection',
            default=False,
            dest='restart',
        )
        sp_tpg_256a.add_argument(
            '--test',
            action='store_true',
            help='perform a connection check',
            default=False,
            dest='test',
        )

    def quit(self):
        """ Stops the daemon, called with message 'quit'.
        This methods overrides the original
        :meth:`~Server.quit` to do proper clean-up
        of the database and device handler.
        """
        self.reply = 'See you!'

    def status(self):
        self.reply = 'doing great!'

    def tpg_256a(self):
        """ Modifies or checks the status of the TPG 256A device. """
        self.reply = ''
        # Turn ON
        if self.namespace.turn_on:
            # Check current status
            if self.handle.connected:
                self.logger.info('Device already connected')
                self.reply += 'Device already connected\n'
            else:
                try:
                    self.handle.connect()
                except SerialException as e:
                    self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    self.reply += 'Connection successful\n'

        # Turn OFF
        if self.namespace.turn_off:
            # Check current status
            if not self.handle.connected:
                self.logger.info('Device already off')
                self.reply += 'Device already off'
            else:
                try:
                    self.handle.disconnect()
                except SerialException as e:
                    self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    self.reply += 'Device is now off'

        # Restart
        if self.namespace.restart:
            # TODO
            pass

        # Test
        if self.namespace.test:
            # Check current status
            if not self.handle.connected:
                self.reply += 'Device is not connected, cannot perform test'
            else:
                try:
                    # Read some device information
                    firmware = self.handle.program_number()
                except SerialException as e:
                    self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    self.reply += 'Connection test successful, device firmware: {}'.format(firmware)
                    self.logger.debug('Device firmware: {}'.format(firmware))
