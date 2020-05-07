""" Driver for the Pfeiffer TPG 256A. The device is
a six-channel pressure readout and monitor controller.

The driver has been adapted to Python3 from the
:obj:`PyExpLabSys<PyExpLabSys.drivers.pfeiffer>` library.
"""

import time
from serial import Serial
from serial.serialutil import SerialException
import logging
from typing import List, Tuple
import configparser

# Code translations constants
MEASUREMENT_STATUS = {
    0: 'Measurement data okay',
    1: 'Underrange',
    2: 'Overrange',
    3: 'Sensor error',
    4: 'Sensor off (IKR, PKR, IMR, PBR)',
    5: 'No sensor (output: 5,2.0000E-2 [mbar])',
    6: 'Identification error'
}
GAUGE_IDS = {
    'TPR':      'Pirani Gauge or Pirani Capacitive gauge',
    'IKR9':     'Cold Cathode Gauge 10E-9 ',
    'IKR11':    'Cold Cathode Gauge 10E-11 ',
    'PKR':      'FullRange CC Gauge',
    'PBR':      'FullRange BA Gauge',
    'IMR':      'Pirani / High Pressure Gauge',
    'CMR':      'Linear gauge',
    'noSEn':    'no SEnsor',
    'noid':     'no identifier'
}


class TPG_256A(object): # noqa (ignore CamelCase convention)
    """ Driver for the Pfeiffer TPG 256A. The device is
    a six-channel pressure readout and monitor controller. The
    driver has been adapted to Python3 from the
    :obj:`PyExpLabSys<PyExpLabSys.drivers.pfeiffer>` library, and
    implements the following 6 commands out the 39 in the
    :download:`documentation <../../Pfeiffer_MultiGauge256A_OpInstructions.pdf>`:

    +---------------+-----------------------------------------------------------+
    | Mnemonic      |  Description                                              |
    +===============+===========================================+===============+
    | PNR           | Program number (firmware version)                         |
    +---------------+-----------------------------------------------------------+
    | PR[1 ... 6]   | Pressure measurement (measurement data) gauge [1 ... 6]   |
    +---------------+-----------------------------------------------------------+
    | PRX           | Pressure measurement (measurement data) gauge [1 ... 6]   |
    +---------------+-----------------------------------------------------------+
    | TID           | Transmitter identification (gauge identification)         |
    +---------------+-----------------------------------------------------------+
    """

    # Attributes
    ETX = chr(3)    #: End text (Ctrl-c), chr(3), \\x03
    CR = chr(13)    #: Carriage return, chr(13), \\r
    LF = chr(10)    #: Line feed, chr(10), \\n
    ENQ = chr(5)    #: Enquiry, chr(5), \\x05
    ACK = chr(6)    #: Acknowledge, chr(6), \\x06
    NAK = chr(21)   #: Negative acknowledge, chr(21), \\x15

    # Serial port configuration
    serial: Serial = None                           #: Serial port handler.
    baud_rate: int = 9600                           #: Baud rate for serial communication.
    serial_port: str = '/dev/PfeifferTPG256A'       #: Physical address of the device file.
    timeout: float = 1.0                            #: Time-out for serial connection error.

    # Device setup
    channel_info: List[Tuple[bool, bool, str]] = []   #: Channel information, loaded from the configuration file.

    # Others
    connected: bool = False         #: Status flag.
    logger: logging.Logger = None   #: Single logger for the whole object

    def __init__(self,
                 serial_port: str = None,
                 baud_rate: int = None,
                 connect: bool = False,
                 timeout: float = None,
                 config_file: str = None,
                 ):
        """ Initializes the :class:`TPG_256A` object. If a
        :paramref:`~TPG_256A.__init__.config_file` is given,
        calls the :meth:`config`. If the
        :paramref:`~TPG_256A.__init__.connect` flag is set to
        `True`, attempts the connection to the device.

        Parameters
        ----------
        serial_port : str, optional
            Physical address of the device file, default is 'None'

        timeout : float, optional
            Serial communication time out, default is 'None'

        baud_rate: int, optional
            Baud rate for serial communication, default is 'None'

        connect: bool, optional
            If set, attempt connection to the device, default is `False`

        config_file : str, optional
            Configuration file, default is `None`.

        Raises
        ------
        :class:`SerialException`
            The connection to the device has failed
        """

        # Initialize variables
        self.logger = logging.getLogger('TPG-256A')
        self.connected = False
        for ch in range(0, 6):  # Loop from 0 to 6, but we will only use 1 to 6
            self.channel_info.append((False, False, ''))

        # Load config file, if given
        if config_file is not None:
            self.config(config_file)

        # Assign attributes, if given
        # They override they configuration file
        if baud_rate is not None:
            self.baud_rate = baud_rate
        if serial_port is not None:
            self.serial_port = serial_port
        if timeout is not None:
            self.timeout = timeout

        # Connect to the device
        if connect:
            self.connect()

    def config(self, config_file: str):
        """ Loads the TPG-256A configuration from a file.

        Parameters
        ----------
        config_file : str
            Configuration file to be loaded.

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error
        """

        # Use a logger named like the module itself
        self.logger.info("Loading configuration file %s", config_file)

        try:
            # Initialize config parser and read file
            config_parser = configparser.ConfigParser()
            config_parser.read(config_file)

            # Load serial port configuration
            self.serial_port = config_parser.get(section='Connection', option='device')
            self.baud_rate = config_parser.getint(section='Connection', option='baud_rate')
            self.timeout = config_parser.getfloat(section='Connection', option='timeout')

            # Load channel information
            for ch in range(1, 6):
                sec_name = 'Sensor_%d'.format(ch)
                act = False
                log = False
                lab = None
                if config_parser.has_section(sec_name):
                    act = config_parser.getboolean(sec_name, 'active')
                    log = config_parser.getboolean(sec_name, 'logging')
                    lab = config_parser.get(sec_name, 'label')
                self.channel_info[ch] = (act, log, lab)

        except configparser.Error as e:
            self.logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            self.logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def connect(self):
        """ Connects to the TPG_256A Controller."""
        self.logger.info('Connecting to TPG_256A Controller on port %s', self.serial_port)
        try:
            self.serial = Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                timeout=self.timeout,
            )
        except SerialException as e:
            self.logger.error("{}: {}".format(type(e).__name__, e))
            raise
        else:
            self.connected = True
            self.logger.info('Connection successful')

    def disconnect(self):
        """ Closes the connection to the TPG_256A Controller."""
        # Check the device is connected
        if not self.connected:
            return

        self.logger.info('Closing connection to TPG_256A Controller on port %s', self.serial_port)
        try:
            self.connected = False
            self.serial.close()
        except SerialException as e:
            self.logger.error("{}: {}".format(type(e).__name__, e))
            raise
        else:
            self.logger.info('Connection closed')

    def _cr_lf(self, string):
        """Pad carriage return and line feed to a string

        :param string: String to pad
        :type string: str
        :returns: the padded string
        :rtype: str
        """
        return string + self.CR + self.LF

    def _send_command(self, command):
        """Send a command and check if it is positively acknowledged

        :param command: The command to send
        :type command: str
        :raises IOError: if the negative acknowledged or a unknown response
            is returned
        """
        self.serial.write(str.encode(self._cr_lf(command)))
        response = self.serial.readline().decode()
        if response == self._cr_lf(self.NAK):
            message = 'Serial communication returned negative acknowledge'
            raise IOError(message)
        elif response != self._cr_lf(self.ACK):
            message = 'Serial communication returned unknown response:\n{}'\
                ''.format(repr(response))
            raise IOError(message)

    def _get_data(self):
        """Get the data that is ready on the device

        :returns: the raw data
        :rtype:str
        """
        self.serial.write(str.encode(self.ENQ))
        data = self.serial.readline().decode()
        return data.rstrip(self.LF).rstrip(self.CR)

    def _clear_output_buffer(self):
        """Clear the output buffer"""
        time.sleep(0.1)
        just_read = 'start value'
        out = ''
        while just_read != '':
            just_read = self.serial.read()
            out += just_read
        return out

    def program_number(self):
        """Return the firmware version

        :returns: the firmware version
        :rtype: str
        """
        self._send_command('PNR')
        return self._get_data()

    def pressure_gauge(self, gauge_nr) -> Tuple[int, Tuple[int, str]]:
        """Reads the pressure measured by gauge number
        :paramref:`~TPG_256A.pressure_gauge.gauge`.

        Arguments
        ---------
        gauge_nr: int
            The gauge number, 1 to 6

        Returns
        -------
        Tuple[int, Tuple[int, str]]:
            (value, (status_code, status_message))
        """
        # Check gauge number
        if gauge_nr not in range(1, 6):
            message = 'The input gauge number must be between 1 and 6'
            raise ValueError(message)

        # Perform request
        self._send_command('PR' + str(gauge_nr))
        reply = self._get_data()
        status_code = int(reply.split(',')[0])
        value = float(reply.split(',')[1])
        return value, (status_code, MEASUREMENT_STATUS[status_code])

    def pressure_gauges(self) -> List[Tuple[int, Tuple[int, str]]]:
        """Reads the pressure measured by all gauge.


        Returns
        -------
        List[Tuple[int, Tuple[int, str]]]:
            List of six tuples (value, (status_code, status_message))
        """
        ret = []
        for gauge in range(1, 6):
            ret.append(self.pressure_gauge(gauge))
        return ret

    def gauge_identification(self) -> List[Tuple[str, str]]:
        """Reads the gauge identifications.

        Returns
        -------
        List[Tuple[str, str]]:
            List of six tuples (id_code, gauge_description)
        """

        self._send_command('TID')
        reply = self._get_data()
        id_list = reply.split(',')

        return [(id_code, GAUGE_IDS[id_code]) for id_code in id_list]
