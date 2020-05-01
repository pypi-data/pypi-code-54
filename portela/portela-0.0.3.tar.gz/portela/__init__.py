# -*- encoding: utf-8 -*-
from __future__ import print_function
import sys
import os
import socket
import subprocess
import argparse
import psutil
import textwrap
import fcntl
import struct
from os.path import expanduser
from portela.daemon import Daemon
from portela.shared import Color as c
from portela.shared import all_interfaces

user_home = expanduser("~")

def _get_iface_ip(interface):
    ''' returns IP address of an interface '''
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', interface[:15].encode('utf-8')))[20:24])


def _get_network(interface=None):
    ''' get primary IP of your host '''

    if interface:
        ifaces = all_interfaces()

        if not interface in ifaces:
            print(c.YELLOW + 'interface name %s is not valid. Valid interfaces: %s' % (interface, ifaces) + c.END)
            sys.exit()

        IP = _get_iface_ip(interface)

        if IP:
            return IP
        else:
            print(c.RED + 'cannot determine IP address for interface %s' % interface + c.END)
            sys.exit()
        
    else:
        # add your primary IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except OSError as err:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


def _serve(args):
    ''' start a local webserver on a port '''
 
    port = str(args.port)
   

    if not port.isdigit():
        print(c.YELLOW + 'pass a numeric port, ie: 7500' + c.END)
        sys.exit()

    ## check python version thats currently running Portela
    # Python 2
    if sys.version_info[0] is 2:
        import SimpleHTTPServer
        import SocketServer
        http_handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        http_server = SocketServer.TCPServer

    # Python 3
    elif sys.version_info[0] is 3:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        http_handler = BaseHTTPRequestHandler
        http_server = HTTPServer

    else:
        print('Python version mismatch, only comptabile with Python2 or Python3')
        sys.exit()

    IP = _get_network(args.interface)


    class Handler(http_handler):
            
        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def _msg(self, message):
            return message.encode("utf8")  # NOTE: must return a bytes object!

        def do_GET(self):

            if not args.message:
                message = 'Portela!'
            else:
                message = str(args.message)

            self._set_headers()
            self.wfile.write(self._msg(message))

        def do_HEAD(self):
            self._set_headers()

        def do_POST(self):
            # Doesn't do anything with posted data
            self._set_headers()
            self.wfile.write(self._msg("POST!"))

    server = http_server((IP, int(port)), Handler)
    print('\n' + c.GREEN + 'Portela serving on port: ' + port + c.END)
    print(c.GREEN + 'Connect to this machine using netcat or curl: ' + c.END)
    print(c.TEAL + 'nc -zv ' + IP + ' ' + port + c.END)
    print(c.TEAL + 'curl http://' + IP + ':' + port + c.END +'\n')
    return server.serve_forever()


def _main(args, action='status'):
    """ start the server either as daemon or standalone """

    class PortelaDaemon(Daemon):
        def run(self):
            while True:
                _serve(args)
    
    d = PortelaDaemon(user_home + '/.portela.pid')

    if args.action == 'start':
        
        if args.daemon:
            d.start()
            
        else:
            _serve(args)

    if args.action == 'stop':
        d.stop()

    if args.action == 'status':
        d.status()

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''

    A Simple Port Listener

    portela serve 5432                  (listens on port 5432)
    portela serve 5432 -m 'Hello there' (listens on port 5432 and outputs message)
    portela serve 5432 -i eth1          (listens on port 5432 interface eth1)
    portela serve 5432 -d               (run in background as daemon)
    portela stop                        (stop all portela instances)
    portela status                      (check if any portela ports are up)

    '''))


subparsers = parser.add_subparsers()
serve_parser = subparsers.add_parser('serve', help='serve HTTP listener on a port')
serve_parser.add_argument('port', help='port to listen on', type=int)
serve_parser.add_argument('-m', '--message', action='store', help='message to output during HTTP connection')
serve_parser.add_argument('-d', '--daemon', action='store_true', default=False, help='run Portela as a daemon')
serve_parser.add_argument('-i', '--interface', action='store', default=False, help='run Portela on specific interface or IP')
serve_parser.set_defaults(func=_main, action='start')

stop_parser = subparsers.add_parser('stop')
stop_parser.set_defaults(func=_main, action='stop')

status_parser = subparsers.add_parser('status')
status_parser.set_defaults(func=_main, action='status')

def entry():
    args = parser.parse_args()
    
    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    
    args.func(args)  # call the default function
