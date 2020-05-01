# -*- coding: utf-8 -*-
# uc_daemon - A set of classes and functions for demonizing a process and related tools..
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
A set of classes and functions for demonizing a process and related tools..
"""
import os
import sys
from time import sleep
from multiprocessing import Queue
import logging


# Set default logger.
LOGGER = logging.getLogger()


def __wait_daemon(queue):
    """
    Waits until the daemonized process id appears in the queue.
    Returns daemonized process id on successful and less than zero on fails.
    """
    try:
        while queue.qsize() == 0:
            sleep(0.01)
    except KeyboardInterrupt:
        LOGGER.debug("Awaiting demonization has occurred unforeseen situation.")
        return -1

    return queue.get()


def daemonize():
    """
    Become a daemon.
    To base process returns daemonized process id on successful and less than zero on fails.
    To daemonized process returns zero.
    """
    queue = Queue()
    # Do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
    except OSError as err:
        LOGGER.debug("Fork #1 failed: (%d) %s.", err.errno, err.strerror)
        return -2
    else:
        if pid > 0:
            return __wait_daemon(queue)

    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # Do second fork
    try:
        pid = os.fork()
    except OSError as err:
        LOGGER.debug("Fork #2 failed: (%d) %s.", err.errno, err.strerror)
        queue.put(-3)
    else:
        if pid > 0:
            sys.exit(0)

    # When everything is done inform the base process to free it.
    queue.put(os.getpid())
    # Returns zero to daemonized process
    return 0


def redirectio(handle):
    """
    Redirects standart descriptors
    """
    try:
        sys.stdout.flush()
        sys.stderr.flush()

        sout = None
        serr = None

        if handle is None:
            sout = open('/dev/null', 'a+')
            serr = open('/dev/null', 'a+')
        else:
            sout = handle
            serr = handle

        os.dup2(sout.fileno(), sys.stdout.fileno())
        os.dup2(serr.fileno(), sys.stderr.fileno())
    except OSError as err:
        sys.stderr.write("Redirect IO failed: (%d) %s\n\r" % (err.errno, err.strerror))
