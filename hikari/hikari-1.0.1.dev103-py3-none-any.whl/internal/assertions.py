#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekokatt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""Assertions of things.

These are functions that validate a value, and are expected to return the value
on success but error on any failure. This allows for quick checking of
conditions that might break the function or cause it to misbehave.
"""

from __future__ import annotations

__all__ = [
    "assert_that",
    "assert_not_none",
    "assert_none",
    "assert_in_range",
    "assert_is_int_power",
]

import math
import typing

ValueT = typing.TypeVar("ValueT")


def assert_that(
    condition: bool, message: typing.Optional[str] = None, error_type: typing.Type[BaseException] = ValueError
) -> None:
    """If the given condition is falsified, raise a `ValueError`.

    Will be raised with the optional description if provided.
    """
    if not condition:
        raise error_type(message or "condition must not be False")


def assert_not_none(value: ValueT, message: typing.Optional[str] = None) -> ValueT:
    """If the given value is `None`, raise a `ValueError`.

    Will be raised with the optional description if provided.
    """
    if value is None:
        raise ValueError(message or "value must not be None")
    return value


def assert_none(value: ValueT, message: typing.Optional[str] = None) -> ValueT:
    """If the given value is not None, raise a ValueError.

    Will be raised with the optional description if provided.
    """
    if value is not None:
        raise ValueError(message or "value must be None")
    return value


def assert_in_range(
    value: ValueT, min_inclusive: float, max_inclusive: float, name: typing.Optional[str] = None
) -> ValueT:
    """If a value is not in the range [min, max], raise a `ValueError`."""
    if not min_inclusive <= value <= max_inclusive:
        name = name or "The value"
        raise ValueError(f"{name} must be in the inclusive range of {min_inclusive} and {max_inclusive}")
    return value


def assert_is_int_power(value: int, power: int) -> int:
    """If a value is not a power the given int, raise `ValueError`."""
    logarithm = math.log(value, power)
    assert_that(logarithm.is_integer(), f"value must be an integer power of {power}")
    return value
