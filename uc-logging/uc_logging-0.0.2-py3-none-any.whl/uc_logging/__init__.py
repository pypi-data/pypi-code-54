# uc_logging - A set of classes and functions that extend the log package.
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
A set of classes and functions that extend the log package.
"""
import os
import logging


class Formatter(logging.Formatter):
    """
    Multi formatter.
    Adds the ability to format log messages based on their level.
    """
    def __init__(self, default=logging.BASIC_FORMAT, formats=None):
        """
        Formats is a dict where key is a level
        and value it's a format.
        """
        if formats is not None and not isinstance(formats, dict):
            raise TypeError("formats must be a dict type. %s given" % type(formats))

        self.formats = formats
        super(Formatter, self).__init__(default)

    def format(self, record):
        """
        Format the record depending on a level
        """
        # Store original format
        original_format = self._style._fmt # pylint: disable=protected-access
        # Switch format
        if self.formats is not None and record.levelno in self.formats:
            self._style._fmt = self.formats[record.levelno] # pylint: disable=protected-access
        # Call to original formatter
        message = super(Formatter, self).format(record)
        # Restore original format
        self._style._fmt = original_format # pylint: disable=protected-access

        return message


class UnbufferedStreamHandler(logging.StreamHandler):
    """
    Unbuffered stream handler.

    When multiprocessing queue is used (for example),
    standard output may be stuck. Common flushing
    not working. Using -u option not guaranteed (it helps).
    So write directly.
    """
    def emit(self, record):
        # We just write to stream dircetly.
        message = self.format(record) + self.terminator
        os.write(self.stream.fileno(), message.encode())
