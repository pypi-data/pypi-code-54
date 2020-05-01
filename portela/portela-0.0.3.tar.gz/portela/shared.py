import socket
import fcntl
import struct
import array
import sys

class Color:
    GREEN = '\x1b[0;32;40m' 
    BLUE = '\x1b[0;34;40m' 
    YELLOW = '\x1b[0;33;40m'
    TEAL = '\x1b[0;36;40m'
    WHITE = '\x1b[0;37;40m'
    RED = '\x1b[1;31;40m'
    GRAY = '\x1b[2;37;40m'
    END = '\x1b[0m'

def all_interfaces():
    ''' get all network interface names '''
    
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    names = array.array("B", '\0'.encode('UTF-8') * bytes) 
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    lst = []
    for i in range(0, outbytes, 40):
        name = namestr[i:i+16].split('\0'.encode('UTF-8'), 1)[0]
        ip   = namestr[i+20:i+24]

        if sys.version_info[0] is 2:
            lst.append(name)
        if sys.version_info[0] is 3:
            lst.append(name.decode('UTF-8'))
    return lst

def format_ip(addr):
    return str(ord(addr[0])) + '.' + \
           str(ord(addr[1])) + '.' + \
           str(ord(addr[2])) + '.' + \
           str(ord(addr[3]))
