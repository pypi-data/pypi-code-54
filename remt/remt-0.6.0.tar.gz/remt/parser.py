#
# remt - reMarkable tablet command-line tools
#
# Copyright (C) 2018-2019 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
reMarkable tablet lines format parser.
"""

import struct

from .data import *
from .util import flatten


HEADER_START = b'reMarkable .lines file, version='
FMT_HEADER_PAGE = struct.Struct('<{}ss10s'.format(len(HEADER_START)))
FMT_PAGE = struct.Struct('<BBH')  # TODO: might be 'I'
FMT_LAYER = struct.Struct('<I')
FMT_STROKE = struct.Struct('<IIIfI')
FMT_STROKE_V5 = struct.Struct('<IIIfII')
FMT_SEGMENT = struct.Struct('<ffffff')


def parse_item(fmt, fin):
    """
    Read number of bytes from a file and parse the data of a drawing item
    using a format.

    :param fmt: Struct format object.
    :param fin: File object.
    """
    buff = fin.read(fmt.size)
    return fmt.unpack(buff)

def parse_segment(n_seg, data):
    x, y, speed, direction, width, pressure = parse_item(FMT_SEGMENT, data)
    return Segment(n_seg, x, y, speed, direction, width, pressure)

def parse_stroke(ver, n_stroke, data):
    if ver == '5':
        pen, color, _, width, _, n = parse_item(FMT_STROKE_V5, data)
    elif ver == '3':
        pen, color, _, width, n = parse_item(FMT_STROKE, data)
    else:
        assert False, 'unknown version {}'.format(ver)

    segments = [parse_segment(i, data) for i in range(n)]
    stroke = Stroke(n_stroke, pen, color, width, segments)

    yield stroke

def parse_layer(ver, n_layer, data):
    n, = parse_item(FMT_LAYER, data)

    items = (parse_stroke(ver, i, data) for i in range(n))

    yield Layer(n_layer)
    yield from flatten(items)

def parse_page(ver, data, page_number):
    n, _, _ = parse_item(FMT_PAGE, data)
    items = (parse_layer(ver, i, data) for i in range(n))

    yield Page(page_number)
    yield from flatten(items)
    yield PageEnd(page_number)

def parse(data, page_number):
    header, ver, *_ = parse_item(FMT_HEADER_PAGE, data)
    ver = ver.decode()
    assert header.startswith(HEADER_START), 'header is {!r}'.format(header)
    assert ver in ('3', '5'), 'version is {}'.format(ver)

    yield from parse_page(ver, data, page_number)

def empty_page(page_number):
    """
    Generate empty page for document rendering.

    :param page_number: Page number to be associated with the page.
    """
    yield Page(page_number)
    yield PageEnd(page_number)

# vim: sw=4:et:ai
