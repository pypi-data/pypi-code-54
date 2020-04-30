# -*- coding: utf-8 -*-
# uc_pidfile - A set of classes and functions for managing pidfile.
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
A set of classes and functions for managing pidfile.
"""
import os
import atexit


def process_exists(pid):
    """
    Checks if the process is running.

    Returns True if process exists and False if not.
    """
    try:
        os.kill(pid, 0)
    except PermissionError:
        # Process exists, so yes
        return True
    except ProcessLookupError:
        return False
    else:
        return True


def read_pid(filename):
    """
    Reads pid from file.

    If the file exists and is successfully read,
    then returns pid otherwise returns None.

    May raise exceptions:
        PermissionError
        ValueError
    """
    pid = None

    try:
        with open(filename, "r") as handle:
            pid = int(handle.readline().strip())
    except FileNotFoundError:
        pass

    return pid


def validate_pidfile(filename):
    """
    Checks the contents of pidfiles for an integer.

    Returns True if valid or False if not.

    May raise exceptions:
        FileNotFoundError
        PermissionError
    """
    try:
        pid = read_pid(filename)
    except ValueError:
        return False
    else:
        return pid is not None


def is_running(filename):
    """
    Returns True if the process is running.
    Otherwise returns False.
    """
    try:
        pid = read_pid(filename)
        if pid is not None and process_exists(pid):
            return True
    except FileNotFoundError:
        # We believe that if there is no file, then the process was not started.
        return False
    except PermissionError:
        # We believe that if the file is there, then the process was started.
        return True
    except ValueError:
        # Something went wrong when the program started. We believe that this does not work.
        return False
    else:
        return False


class PidFile:
    """
    Create/Remove pidfile.

    Note:
        I see no reason to lock the pid file.
        Moreover, practice has shown that locks
        do not protect a file from being deleted or overwritten.
    """
    def __init__(self, filename, overwrite=False):
        """
        Creates pid file.

        May raise exceptions:
            FileExistsError
            PermissionError
            FileNotFoundError (If the target directory does not exist, for example.)
        """
        self.__filename = filename
        atexit.register(self.atexit)

        if os.path.isfile(self.filename) and not overwrite:
            raise FileExistsError("File '%s' already exists." % self.filename)

        with open(self.filename, "w") as handle:
            handle.write("%d" % os.getpid())
            handle.flush()

    @property
    def filename(self):
        """
        Returns name of the pid file.
        """
        return self.__filename

    def atexit(self):
        """
        Deletes the pid file before the programm terminates.
        """
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass
