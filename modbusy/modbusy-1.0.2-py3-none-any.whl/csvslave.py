# Copyright (c) 2020, 8minute Solar Energy LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Script to emulate a Modbus slave using values read from a CSV file"""

import contextlib
import csv
import logging
import re
import warnings
from typing import Any, Callable, Dict, Iterator, List, Optional, TextIO, Tuple, Type, Union

import click
from umodbus.utils import log_to_stream
import voluptuous
import voluptuous.humanize
import yaml

import modbusy


def _data_loop(input_file: TextIO, dialect: Optional[Type[csv.Dialect]],
               skip: int = 0) -> Iterator[Tuple[list, int]]:
    """Infinitely loop over values in a CSV file

    input_file is a file-like object to a seekable file. dialect is the
    CSV dialect describing the format of the CSV file. And skip is the
    number of rows to skip at the top of the file (to skip headers).

    An iterator of 2-tuples is returned. The first value is a list of
    values read from the next row. The second value is the row number
    and is useful for error reporting.
    """
    while True:
        input_file.seek(0)  # Rewind the file
        reader = csv.reader(input_file, dialect)  # type: ignore[arg-type]
        for _ in range(skip):  # Skip over the header
            next(reader)
        count = 0
        for row in reader:  # Iterate over the remaining rows
            yield row, reader.line_num
            count += 1
        if not count:
            while True:
                yield [], 0


class Register:
    """Provides class attribute access to register definitions

    All the attributes of this class are validated by voluptuous before
    the object is instantiated. This class simply provides type-checked
    access to the register dictionaries using object attribute syntax.
    """
    address: int
    column: Optional[Union[int, str]]
    value: Union[bool, float, int, str]
    type: modbusy.RegisterType
    trigger: bool
    slave_id: Optional[int]
    byteorder: Optional[str]
    mixed: Optional[bool]

    def __init__(self, reg: dict) -> None:
        self.__dict__ = reg
        self.parse = get_parser(self.type)


def _string(value: Any) -> bytes:
    """Parse a string value and return UTF-8 encoded bytes"""
    return str(value).encode('utf-8')


# Parser function mapping used to map register types to parse functions
_parse_functions: Dict[Type[modbusy.RegisterType], Callable[[Any], Any]] = {
    modbusy.Float: float,
    modbusy.Integer: int,
    modbusy.Boolean: voluptuous.Boolean(),
    modbusy.String: _string,
}


def get_parser(kind: modbusy.RegisterType) -> Callable[[Any], Any]:
    """Lookup a parser given a register type

    If a register type doesn't already exist in the map, the items in
    the map ar iterated until a base class is found and the parser for
    that base class is inherited.
    """
    try:
        return _parse_functions[kind.__class__]
    except KeyError:
        for cls, parse in _parse_functions.items():
            if isinstance(kind, cls):
                _parse_functions[kind.__class__] = parse
                return parse
    assert False, f'failed to find a parser for type {type!r}'


def validate(config: dict) -> dict:
    """Validate a configuration file and return the validated dictionary

    Raises some sort of voluptuous.Error if validation fails. Some
    values are coerced into appropriate types and optional keys receive
    either default values or are set to None.
    """
    v = voluptuous

    def register_type(value: str) -> modbusy.RegisterType:
        try:
            value = value.lower()
        except AttributeError:
            pass
        else:
            if value in ['bool', 'float', 'int16', 'int32', 'int64', 'int128',
                         'double', 'uint16', 'uint32', 'uint64', 'uint128']:
                return getattr(modbusy, value.upper())
        try:
            match = re.match(r'string\[(\d+)\]', value, re.I)
        except TypeError:
            pass
        else:
            if match:
                return modbusy.String(int(match.group(1)))
        raise v.Invalid('invalid register type')

    return v.Schema({
        v.Optional('slave_id', default=1): v.All(int, v.Range(1, 255)),
        v.Optional('byteorder', default='big'): v.In(['big', 'little']),
        v.Optional('mixed', default=False): v.All(v.truth(lambda x: x is not None), v.Boolean()),
        'registers': v.All(
            [v.All(
                {
                    'address': v.Any(
                        v.All(int, v.Range(0, 65535)),
                        [v.All(int, v.Range(0, 65535))]
                    ),
                    v.Optional('column', default=None): v.Any(None, str, int),
                    v.Optional('value', default=None): v.Any(None, float, int, str, v.Boolean()),
                    v.Optional('type', default='int16'): register_type,
                    v.Optional('trigger', default=False): v.Boolean(),
                    v.Optional('slave_id', default=None): v.Any(None, v.All(int, v.Range(1, 255))),
                    v.Optional('byteorder', default=None): v.In(['big', 'little', None]),
                    v.Optional('mixed', default=None): v.Any(None, v.Boolean()),
                },
                v.Any(
                    {'column': v.Any(str, int), 'value': None, v.Extra: object},
                    {'type': v.Any(modbusy.Float, modbusy.Double),
                     'value': v.All(v.DefaultTo(0.0), v.Coerce(float)), v.Extra: object},
                    {'type': modbusy.Boolean,
                     'value': v.All(v.DefaultTo(False), v.Boolean()), v.Extra: object},
                    {'type': modbusy.String,
                     'value': v.All(v.DefaultTo(''), v.Coerce(_string)), v.Extra: object},
                    {'value': v.All(v.DefaultTo(0), v.Coerce(int)), v.Extra: object},
                    msg='value is not of the given type'
                ),
            )],
        ),
    }, required=True, extra=v.REMOVE_EXTRA)(config)


@modbusy.tcp_app()
@click.argument('config', type=click.File())
@click.argument('data', type=click.File())
@contextlib.contextmanager
def main(app: modbusy._Server, config: TextIO, data: TextIO) -> Iterator[None]:
    """Modbus slave that reads values from a CSV file"""
    log_to_stream(level=logging.DEBUG)

    # Parse the configuration and validate it against a schema
    with config:
        config_dict = yaml.safe_load(config)
    try:
        config_dict = validate(config_dict)
    except voluptuous.Error as exc:
        errors = voluptuous.humanize.humanize_error(config_dict, exc).split('\n')
        try:
            error, = errors
        except ValueError:
            error = '\n  '.join(['', *errors])
        raise click.ClickException(f'{config.name}: {error}')

    # Sample the top of the file to autodetect dialect and headers
    sample = data.read(4096)
    data.seek(0)  # Rewind the file after taking the sample
    sniffer = csv.Sniffer()
    try:
        dialect: Optional[Type[csv.Dialect]] = sniffer.sniff(sample)
        has_header = sniffer.has_header(sample)
    except csv.Error:
        dialect = None
        has_header = False
    reader = csv.reader(data, dialect)  # type: ignore[arg-type]
    try:
        row: List[Any] = next(reader)
    except StopIteration:
        row = []
    headers: Dict[Union[str, int], int] = {i: i for i in range(len(row))}
    if has_header:
        headers.update((key, i) for i, key in enumerate(row) if key)
        row = next(reader)  # Get the first row of data
        skip = 1
    else:
        skip = 0

    # Initialize a loop over the CSV file
    loop = _data_loop(data, dialect, skip)
    registers: List[Optional[Register]] = [None] * len(row)

    def read_row() -> None:
        """Reads the next row and updates the list with parsed values"""
        row, line_num = next(loop)
        for reg, (colnum, col) in zip(registers, enumerate(row, 1)):
            if reg:
                try:
                    reg.value = reg.parse(col)
                except (ValueError, voluptuous.Invalid, TypeError):
                    warnings.warn(f'failed to parse value {col!r} '
                                  f'at line {line_num}, column {colnum}')

    # Update server defaults to match configuration
    app.update_defaults(slave_id=config_dict['slave_id'],
                        byteorder=config_dict['byteorder'],
                        mixed=config_dict['mixed'])

    def decorate(reg: Register) -> None:
        if reg.trigger:
            def read(for_write: bool) -> Any:
                if not for_write:
                    read_row()
                return reg.value
        else:
            def read(for_write: bool) -> Any:
                return reg.value
        app.register(reg.address, reg.type, slave_id=reg.slave_id,
                     byteorder=reg.byteorder, mixed=reg.mixed)(read)

    # Add registers to the slave
    for reg in (Register(r) for r in config_dict['registers']):
        decorate(reg)

        if reg.column is None:
            continue  # Use static value instead of one read from the file

        # Convert string keys to int and verify that column exist
        try:
            colnum = headers[reg.column]
        except KeyError:
            kind = 'name' if isinstance(reg.column, str) else 'index'
            raise click.ClickException(f'{data.name}: no such column {kind}: {reg.column!r}')

        # Initialize values to given value or the first record in the file
        if reg.value is None:
            try:
                reg.value = reg.parse(row[colnum])
            except (ValueError, voluptuous.Invalid, TypeError):
                raise click.ClickException(f'{data.name}: failed to parse value {row[colnum]!r} '
                                           f'at line {reader.line_num}, column {colnum + 1}')
        registers[colnum] = reg
    yield


if __name__ == '__main__':
    main()
