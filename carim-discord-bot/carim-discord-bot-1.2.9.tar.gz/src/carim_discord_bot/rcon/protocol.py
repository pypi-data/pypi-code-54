import logging
import struct
import zlib

# https://www.battleye.com/downloads/BERConProtocol.txt

FORMAT_PREFIX = '='
HEADER_FORMAT = 'BBIB'
PACKET_TYPE_FORMAT = 'B'
SEQUENCE_NUMBER_FORMAT = 'B'
HEADER_SIZE = struct.calcsize(FORMAT_PREFIX + HEADER_FORMAT)
LOGIN = 0x00
COMMAND = 0x01
MESSAGE = 0x02
B = 0x42
E = 0x45
H_END = 0xff
SUCCESS = 0x01

log = logging.getLogger(__name__)


class Packet:
    def __init__(self, payload):
        self.payload = payload

    @staticmethod
    def parse(data):
        try:
            b, e, checksum, f = struct.unpack_from(FORMAT_PREFIX + HEADER_FORMAT, data)
            payload_data = data[HEADER_SIZE:]
            if b == B and e == E and f == H_END and checksum == Packet.checksum(payload_data):
                payload = Payload.parse(payload_data)
                return Packet(payload)
        except (IndexError, struct.error):
            log.warning(f'invalid {data}')
        return None

    def generate(self):
        payload = self.payload.generate()
        return struct.pack(FORMAT_PREFIX + HEADER_FORMAT, B, E, Packet.checksum(payload), H_END) + payload

    @staticmethod
    def checksum(data):
        checksum = zlib.crc32(bytes([H_END]) + data)
        return checksum

    def __str__(self):
        return str(self.payload)


class Payload:
    @staticmethod
    def parse(data):
        packet_type = struct.unpack_from(FORMAT_PREFIX + PACKET_TYPE_FORMAT, data)[0]
        if packet_type == LOGIN:
            return Login.parse(data[1:])
        if packet_type == COMMAND:
            return Command.parse(data[1:])
        if packet_type == MESSAGE:
            return Message.parse(data[1:])
        return None

    def generate(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class Login(Payload):
    def __init__(self, password=None, success=False):
        self.password = password
        self.success = success

    @staticmethod
    def parse(data):
        success_flag = struct.unpack_from(FORMAT_PREFIX + SEQUENCE_NUMBER_FORMAT, data)[0]
        return Login(success=success_flag == SUCCESS)

    def generate(self):
        return struct.pack(FORMAT_PREFIX + PACKET_TYPE_FORMAT, LOGIN) + bytes(self.password, encoding='ascii')

    def __str__(self):
        return f'Login {self.success}'


class Command(Payload):
    def __init__(self, sequence_number, data=None, command=''):
        self.sequence_number = sequence_number
        self.data = data
        self.command = command

    @staticmethod
    def parse(data):
        sequence_number = struct.unpack_from(FORMAT_PREFIX + SEQUENCE_NUMBER_FORMAT, data)[0]
        return Command(sequence_number, data=str(data[1:], encoding='ascii'))

    def generate(self):
        packet = struct.pack(FORMAT_PREFIX + PACKET_TYPE_FORMAT + SEQUENCE_NUMBER_FORMAT, COMMAND, self.sequence_number)
        packet += bytes(self.command, encoding='ascii')
        return packet

    def __str__(self):
        single_line = self.data.replace('\n', '|')
        return f'Command <{single_line}>'


class Message(Payload):
    def __init__(self, sequence_number, message=None):
        self.sequence_number = sequence_number
        self.message = message

    @staticmethod
    def parse(data):
        sequence_number = struct.unpack_from(FORMAT_PREFIX + SEQUENCE_NUMBER_FORMAT, data)[0]
        try:
            message = str(data[1:], encoding='ascii')
        except UnicodeDecodeError:
            message = str(data[1:], encoding='utf-8')
        return Message(sequence_number, message=message)

    def generate(self):
        return struct.pack(FORMAT_PREFIX + PACKET_TYPE_FORMAT + SEQUENCE_NUMBER_FORMAT, MESSAGE, self.sequence_number)

    def __str__(self):
        single_line = self.message.replace('\n', '|')
        return f'Message <{single_line}>'
