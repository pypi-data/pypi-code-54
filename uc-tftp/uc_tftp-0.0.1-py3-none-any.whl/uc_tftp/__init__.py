# -*- coding: utf-8 -*-
# uc_tftp - Implementation of classes and functions for working with files via tftp.
# It is part of the Unicon project.
# https://unicon.10k.me
#
# Copyright © 2020 Eduard S. Markelov.
# All rights reserved.
# Author: Eduard S. Markelov <markeloveduard@gmail.com>
#
# This program is Free Software; you can redistribute it and/or modify it under
# the terms of version three of the GNU Affero General Public License as
# published by the Free Software Foundation and included in the file LICENSE.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
The build script for setuptools.

TODO: class TFTPSender for sending file via tftp.
"""
import os
import sys
import socket
import struct


class NoWRQPacket(Exception):
    """
    Implementation of exception for invalid packet received.
    """
    def __init__(self, opcode):
        opcode_name = ""

        if opcode == 1: # Read request (RRQ)
            opcode_name = "RRQ"
        elif opcode == 3: # Data packet (DATA)
            opcode_name = "DATA"
        elif opcode == 4: # Acknowledgment (ACK)
            opcode_name = "ACK"
        elif opcode == 5: # Error (ERROR)
            opcode_name = "ERROR"

        super(NoWRQPacket, self).__init__("WRQ packet expected, but %s was received." % opcode_name)


class NoIncomingConnection(Exception):
    """
    Implementation of exception for listening timeout.
    """
    def __init__(self):
        super(NoIncomingConnection, self).__init__\
        ("There was no incoming connection for the allotted period of time.")


class ErrorReceived(Exception):
    """
    Implementing an exception for reporting an error message.
    """
    def __init__(self, errorcode, errormsg):
        super(ErrorReceived, self).__init__("Error received: (%d) %s", errorcode, errormsg)


class UnexpectedOpcode(Exception):
    """
    Implementing an exception for unexpected opcode.
    """
    def __init__(self):
        super(UnexpectedOpcode, self).__init__("Unexpected opcode received.")


class TFTPReceiver:
    """
    Simple file receiver via tftp.
    """
    def __init__(self, host="0.0.0.0", timeout=1):
        # last operation code
        self.__opcode = None
        # address for listening
        self.host = host
        # connection waiting timeout
        self.timeout = timeout
        # store initiate address for checking next packets
        self.addr = None
        self.filename = None
        self.mode = None

        self.__initsocket()

    def __readstring(self, data): # pylint: disable=no-self-use
        """
        Reads the zero terminated string
        """
        string = None
        for idx, char in enumerate(data):
            if char == 0:
                string = data[:idx]
                break

        return string


    def __initsocket(self):
        """
        Initializes socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(self.timeout)
        sock.bind((self.host, 69))
        self.sock = sock


    def recvto(self, destination=None):
        """
        Receives file to destination directory.
        """
        # set default destination directory
        if not destination:
            destination = os.path.dirname(os.path.abspath(sys.argv[0]))

        self.__waitconnection()

        with open(os.path.join(destination, self.filename), "w") as file:
            for block in self:
                file.write(block)

    def open(self):
        """
        Same as __waitconnection()
        """
        self.__waitconnection()


    def __waitconnection(self):
        """
        Waits a new connection and first packet.
        If unexpected packet was received will raise exception.
        """
        try:
            data, self.addr = self.sock.recvfrom(516)
        except socket.timeout:
            raise NoIncomingConnection()

        self.__opcode = struct.unpack(">H", data[:2])[0]
        if self.__opcode == 2: # WRQ
            self.filename = self.__readstring(data[2:]).decode()
            self.mode = self.__readstring(data[2 + len(self.filename) + 1:]).decode()
            # send ACK
            self.sock.sendto(struct.pack(">hh", 4, 0), self.addr)
        else:
            raise NoWRQPacket(self.__opcode)


    def __iter__(self):
        """
        Prepares iteration
        """
        if self.__opcode is None:
            self.__waitconnection()

        return self


    def __next__(self):
        """
        Iteration process
        """
        data = addr = None
        # if the first packet is not write request then stop iteration
        if self.__opcode == 2: # WRQ
            while True:
                data, addr = self.sock.recvfrom(516)
                # check if packet received from another sender
                if addr != self.addr:
                    errormsg = "Busy"
                    self.sock.sendto(
                        struct.pack(">hh%dsx" % len(errormsg), 5, 0, errormsg),
                        addr)
                else:
                    break

            opcode = struct.unpack(">H", data[:2])[0]
            if opcode == 3: # DATA
                block = struct.unpack(">H", data[2:4])[0]
                self.sock.sendto(struct.pack(">hh", 4, block), addr)
                # if it is last block
                if len(data) < 516:
                    # change stored opcode to non WRQ for stopping iteration
                    self.__opcode = opcode

                return data[4:].decode()
            elif opcode == 5: # ERROR
                errorcode = struct.unpack(">H", data[2:4])[0]
                errormsg = self.__readstring(data[4:])
                raise ErrorReceived(errorcode, errormsg)
            else:
                raise UnexpectedOpcode()
        else:
            if self.sock is not None:
                self.sock.close()
            raise StopIteration

        return None
