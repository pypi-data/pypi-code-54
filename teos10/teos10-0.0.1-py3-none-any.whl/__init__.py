# teos10: unofficial Python implementation of the TEOS-10 properties of water.
# Copyright (C) 2020  Matthew Paul Humphreys  (GNU GPLv3)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Unofficial Python implementation of the TEOS-10 properties of water."""

from . import (
    constants,
    gibbs,
    properties,
)

__all__ = [
    "constants",
    "gibbs",
    "properties",
]

__author__ = "Humphreys, Matthew P."
__version__ = "0.0.1"
