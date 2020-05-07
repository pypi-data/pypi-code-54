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

"""Simplifies the creation of Modbus slaves

modbusy provides a simple inteface for producing boilerplate code for
interfacing with umodbus while requiring limited knowledge of the
Modbus protocol.

Example:
    # modbusy_example.py
    # Execution: python modbusy_example.py --address 127.0.0.1 --port 5020 12345

    import contextlib
    import click
    import modbusy

    # The order of decorators is important
    @modbusy.tcp_app()
    @click.argument('value', type=int)
    @contextlib.contextmanager
    def main(app, value) -> None:
        '''Modbus emulator to serve a single signed 32-bit value'''

        @app.register(0, modbusy.INT32)
        def read_value(for_write):
            return value

        @read_value.setter
        def write_value(new_value):
            nonlocal value
            value = new_value

        yield

    if __name__ == '__main__':
        main()
"""

import contextlib
import functools
import ipaddress
import itertools
import logging
import struct
import sys
import traceback
from types import MethodType
from typing import (Any, Callable, ContextManager, Dict, Iterable, List,
                    NamedTuple, no_type_check, Optional, Tuple, TypeVar, Union)

import gevent.local
from gevent.server import StreamServer
from umodbus.functions import (READ_COILS, READ_DISCRETE_INPUTS, WRITE_MULTIPLE_COILS,
                               WRITE_SINGLE_COIL, READ_HOLDING_REGISTERS, READ_INPUT_REGISTERS,
                               WRITE_MULTIPLE_REGISTERS, WRITE_SINGLE_REGISTER)
from umodbus.server import tcp


__all__ = ['BOOL', 'INT16', 'INT32', 'INT64', 'INT128', 'UINT16', 'UINT32', 'UINT64', 'UINT128',
           'FLOAT', 'DOUBLE', 'String', 'patch_server', 'tcp_app', 'RegisterType']


_log = logging.getLogger(__name__)
_local = gevent.local.local()

MODBUS_REGISTER_SIZE = 2

_RGET = Callable[[bool], Any]
_RSET = Callable[[Any], None]
_RD = Callable[[int, Callable[[], Any]], int]
_WR = Callable[[int, Callable[[], Any], _RSET, int], None]
_TR = Callable[[int, int, int, int], None]

_T = TypeVar('_T')
_FN = TypeVar('_FN', bound=Callable)


class RegisterType:
    """Base class for implementing read/write functions for registers

    count is the number of 2-byte (16-bit) words required to hold the
    value. It is used to determine valid addresses for a register. It
    may also be used by read/write functions when converting values.

    The functions() method must be implemented by subclasses. See the
    functions() documentation for more information.

    By default, the register is considered as a Modbus holding or input
    register. Use the Boolean class if a coil or discrete input is
    desired.
    """
    READ_ONLY_FUNCTIONS = (READ_INPUT_REGISTERS,)
    READ_FUNCTIONS = (READ_HOLDING_REGISTERS,)
    WRITE_FUNCTIONS = (WRITE_MULTIPLE_REGISTERS, WRITE_SINGLE_REGISTER)

    def __init__(self, count: int) -> None:
        if count < 1:
            raise ValueError(f'count must be an integer greater than or equal to 1; got {count!r}')
        self.count = count

    def __eq__(self, other: Any) -> bool:
        return (self.__class__ == getattr(other, '__class__', None) and
                self.count == other.count)

    def functions(self, byteorder: str, wordorder: str) -> Tuple[_RD, _WR]:
        """Return functions for reading and writing register values

        byteorder and wordorder are either 'big' or 'little' and
        indicate the desired endianness of the value and the returned
        word, respectively. byteorder should be used for packing and
        unpacking the entire value while wordorder should be used for
        packing and unpacking the word being read or written.

        A 2-tuple of callables should be returned. The first value is
        the read function and the second is the write function. Read
        functions take two arguments: the offset (in bytes) from where
        the word should be read and a getter function. It must return
        a 2-byte integer, which is the value taken at the given offset.
        Write functions take four arguments: the offset, getter, setter,
        and value. The getter is used to retrieve the current value,
        which should be updated using the given offset and value, and
        which is then passed to the setter.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.count})'


class Boolean(RegisterType):
    """Implements Modbus coil or discrete input register as a boolean"""

    READ_ONLY_FUNCTIONS = (READ_DISCRETE_INPUTS,)
    READ_FUNCTIONS = (READ_COILS,)
    WRITE_FUNCTIONS = (WRITE_MULTIPLE_COILS, WRITE_SINGLE_COIL)

    def __init__(self) -> None:
        # Boolean types use a single coil/discrete input address
        super().__init__(1)

    def functions(self, byteorder: str, wordorder: str) -> Tuple[_RD, _WR]:
        def read(offset: int, fget: Callable[[], bool]) -> int:
            return int(bool(fget()))
        def write(offset: int, fget: Callable[[], bool], fset: Callable[[bool], None], value: int) -> None:
            fset(bool(value))
        return read, write

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'


class Numeric(RegisterType):
    """Base class for Numeric types"""
    def functions(self, byteorder: str, wordorder: str) -> Tuple[_RD, _WR]:
        pack, unpack = self._formatters(byteorder)
        def read(offset: int, fget: Callable[[], int]) -> int:
            packed = pack(fget())
            return int.from_bytes(packed[offset:offset + MODBUS_REGISTER_SIZE], wordorder)
        def write(offset: int, fget: Callable[[], int], fset: Callable[[int], None], value: int) -> None:
            packed = pack(fget())
            packed = (packed[:offset] + value.to_bytes(MODBUS_REGISTER_SIZE, wordorder) +
                      packed[offset + MODBUS_REGISTER_SIZE:])
            fset(unpack(packed))
        return read, write

    def _formatters(self, byteorder: str) -> Tuple[Callable[[Any], bytes], Callable[[bytes], Any]]:
        """Returns functions to pack and unpack values

        Must be implemented by subclasses.
        """
        raise NotImplementedError


class Integer(Numeric):
    """Integer register type

    count is the number of 2-byte words required to hold the integer.
    If signed is True, the value will be treated as a signed integer.
    Otherwise, it will be treated as unsigned.
    """
    def __init__(self, count: int, signed: bool = False) -> None:
        super().__init__(count)
        self.signed = signed

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.signed == other.signed

    def _formatters(self, byteorder: str) -> Tuple[Callable[[int], bytes], Callable[[bytes], int]]:
        def pack(value: int) -> bytes:
            return value.to_bytes(self.count * MODBUS_REGISTER_SIZE, byteorder, signed=self.signed)
        def unpack(value: bytes) -> int:
            return int.from_bytes(value, byteorder, signed=self.signed)
        return pack, unpack

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.count}, signed={self.signed!r})'


class Float(Numeric):
    """Single-precision floating point number register type"""
    _STRUCTS = {bo: struct.Struct(f'{bom}f') for (bo, bom) in [('big', '>'), ('little', '<')]}

    def __init__(self) -> None:
        super().__init__(self._STRUCTS['big'].size // MODBUS_REGISTER_SIZE)

    def _formatters(self, byteorder: str) -> Tuple[Callable[[float], bytes], Callable[[bytes], float]]:
        st = self._STRUCTS[byteorder]
        def pack(value: float) -> bytes:
            return st.pack(value)
        def unpack(data: bytes) -> float:
            return st.unpack(data)[0]
        return pack, unpack

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'


class Double(Float):
    """Double-precision floating point number register type"""
    _STRUCTS = {bo: struct.Struct(f'{bom}d') for (bo, bom) in [('big', '>'), ('little', '<')]}


class String(RegisterType):
    """String register type

    size is the number of characters desired. The underlying value,
    however, will use 2-byte words, which could result in NULL padding.
    """
    def __init__(self, size: int) -> None:
        if size < 1:
            raise ValueError('string length must be greater than zero')
        super().__init__((size + 1) // MODBUS_REGISTER_SIZE)
        self.size = size

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.size == other.size

    def functions(self, byteorder: str, wordorder: str) -> Tuple[_RD, _WR]:
        def read(offset: int, fget: Callable) -> int:
            packed = fget()[offset:offset + MODBUS_REGISTER_SIZE]
            if len(packed) < MODBUS_REGISTER_SIZE:
                packed = (packed + b'\x00\x00')[:MODBUS_REGISTER_SIZE]
            return int.from_bytes(packed, wordorder)
        def write(offset: int, fget: Callable, fset: Callable, value: int) -> None:
            packed = fget()
            word = value.to_bytes(MODBUS_REGISTER_SIZE, wordorder)
            packed = packed[:offset] + word + packed[offset + MODBUS_REGISTER_SIZE:]
            fset(packed)
        return read, write

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.size})'


BOOL = Boolean()

UINT16 = Integer(1)
UINT32 = Integer(2)
UINT64 = Integer(4)
UINT128 = Integer(8)

INT16 = Integer(1, signed=True)
INT32 = Integer(2, signed=True)
INT64 = Integer(4, signed=True)
INT128 = Integer(8, signed=True)

FLOAT = Float()
DOUBLE = Double()


class _Options(NamedTuple):
    slave_id: int
    byteorder: str
    mixed: bool


# Used solely for type-checking
class _Server:
    route_map: Any
    route: Callable[[Any, List[int], List[int], List[int]], Callable[[_FN], _FN]]
    _default_options: _Options
    register: MethodType
    update_defaults: MethodType

_S = TypeVar('_S', bound=_Server)


def patch_server(server: _S, slave_id: int = 1, byteorder: str = 'big', mixed: bool=False) -> _S:
    """Add register decorator and default options to server object"""
    assert hasattr(server, 'route')
    _validate_slave_id(slave_id)
    _validate_byteorder(byteorder)
    server._default_options = _Options(slave_id, byteorder, mixed)
    server.register = MethodType(Register, server)
    server.update_defaults = MethodType(update_defaults, server)
    return server


def update_defaults(self: _S, slave_id: int = None, byteorder: str = None, mixed: bool = None) -> None:
    if slave_id is not None:
        _validate_slave_id(slave_id)
    else:
        slave_id = self._default_options.slave_id
    if byteorder is not None:
        _validate_byteorder(byteorder)
    else:
        byteorder = self._default_options.byteorder
    if mixed is None:
        mixed = self._default_options.mixed
    self._default_options = _Options(slave_id, byteorder, mixed)


def _validate_slave_id(slave_id: int) -> None:
    if not 0 < slave_id <= 255:
        raise ValueError(f'invalid slave ID: {slave_id!r}')

def _validate_byteorder(byteorder: str) -> None:
    if byteorder not in ['big', 'little']:
        raise ValueError(f"byteorder must be 'big' or 'little'; got {byteorder!r}")

def _validate_address(address: int) -> None:
    if not 0 <= address <= 65535:
        raise ValueError(f'invalid address: {address!r}')


class Register:
    """Decorator for getters and setters of Modbus register values

    server is the umodbus server object generaged by get_server().
    Addresses are zero-based and map directly to a Modbus addresses. No
    checking is done to ensure addresses don't overlap.

    slave_id is an integer indicating the slave and defaults to 1 or to
    the slave_id of the server, if given. byteorder can be 'big' or
    'little' and defaults to 'big' or to the default on the server.
    If mixed is True, the word order is swapped. The default is False or
    the value configured on the server.

    The instance is intended to be used as a decorator on getter
    functions or instance methods. Decorated functions will have a
    setter attribute added to them which may be used to decorate a
    setter function. Once a setter function is decorated, the setter
    attribute will be deleted.

    Arbitrary object attributes may also be used for the register value
    using the attribute() method.
    """
    def __init__(self, server: _Server, address: Union[int, Iterable[int]], kind: RegisterType, *,
                 slave_id: int = None, byteorder: str = None, mixed: bool = None) -> None:
        self.server = server
        self.kind = kind
        addresses: List[int]
        try:
            addresses = list(address)  # type: ignore[arg-type]
        except TypeError:
            addresses = [address]  # type: ignore[list-item]
        for address in addresses:
            _validate_address(address)

        def get_option(value: Optional[_T], name: str, default: _T, validate: Callable = None) -> _T:
            if value is None:
                try:
                    return getattr(server._default_options, name)
                except AttributeError:
                    return default
            if validate:
                validate(value)
            return value

        self.slave_id = get_option(slave_id, 'slave_id', 1, _validate_slave_id)
        byteorder = get_option(byteorder, 'byteorder', 'big', _validate_byteorder)
        mixed = get_option(mixed, 'mixed', False)
        wordorder = 'little' if mixed and kind.count > 1 else 'big'
        self.read_word, self.write_word = kind.functions(byteorder, wordorder)
        self.addr_map = {addr: base for base in addresses for addr in range(base, base + kind.count)}
        # read_codes is a mutable list and defaults to the read-only
        # functions when the getter is decorated. If and when a setter
        # is decorated, the list is updated with read codes for read/
        # write registers.
        self.read_codes = list(self.kind.READ_ONLY_FUNCTIONS)
        self.frame: traceback.FrameSummary
        self.fget: _RGET
        self.fset: _RSET

    def get_value(self, for_write: bool = False) -> Any:
        try:
            return _local.values[self]
        except KeyError:
            _local.values[self] = value = self.fget(for_write)
            return value

    def get_write_value(self) -> Any:
        return self.get_value(True)

    def set_value(self, value: Any) -> None:
        _local.values[self] = value

    def read(self, slave_id: int, function_code: int, address: int) -> int:
        offset = (address - self.addr_map[address]) * MODBUS_REGISTER_SIZE
        return self.read_word(offset, self.get_value)

    def write(self, slave_id: int, function_code: int, address: int, value: int) -> None:
        offset = (address - self.addr_map[address]) * MODBUS_REGISTER_SIZE
        self.write_word(offset, self.get_write_value, self.set_value, value)
        _local.writes[self] = _local.values[self]

    def __call__(self, fget: _RGET, *, depth: int = 1) -> _RGET:
        """Decorate a getter function

        The getter should accept a single boolean argument, which
        indicates the value is being retrieved for a read (if True) or a
        write (if False), and return a value appropriate for the
        register type. A setter() method is added to the getter for
        additionally decorating a setter function. The setter should
        accept a single value, which is the new value for the register.
        Any return value is ignored.
        """
        addresses = list(self.addr_map)
        self.fget = fget
        self.server.route([self.slave_id], self.read_codes, addresses)(self.read)

        # Used by assert_unique_addresses() to provide helpful tracebacks
        frame = sys._getframe(depth)
        co = frame.f_code
        self.frame = traceback.FrameSummary(co.co_filename, frame.f_lineno, co.co_name,
                                            lookup_line=False, locals=frame.f_locals)

        def setter(fset: _RSET) -> _RSET:
            """Decorate a setter function

            Setters should accept a value appropriate for the register
            type.
            """
            self.read_codes[:] = self.kind.READ_FUNCTIONS
            self.fset = fset
            self.server.route([self.slave_id], list(self.kind.WRITE_FUNCTIONS), addresses)(self.write)

            with contextlib.suppress(AttributeError):
                del fget.setter  # type: ignore[attr-defined]
            return fset

        fget.setter = setter  # type: ignore[attr-defined]
        return fget

    def attribute(self, obj: Any, name: str, writable: Union[bool, Callable] = True) -> None:
        """Use an object attribute to store a register value

        obj is the object and name is the attribute name to get and,
        if writable is True, to set.
        """
        def fget(for_write: bool) -> Any:
            return getattr(obj, name)
        self.__call__(fget, depth=2)

        if callable(writable):
            fget.setter(writable)  # type: ignore[attr-defined]
        elif writable:
            @fget.setter  # type: ignore[attr-defined,misc]
            def fset(value: Any) -> None:
                setattr(obj, name, value)


def assert_unique_addresses(server: _Server) -> None:
    """Ensure all register addreses are unique

    Raises AssertionError if registers exist with duplicate addresses.
    The traceback is altered to show the location of the duplicate
    register declaration.
    """
    rules: Dict[Tuple[int, int, int], Callable] = {}
    # Break a rule here and access a private attribute.
    for rule in server.route_map._rules:
        endpoint = rule.endpoint
        for addr in itertools.product(rule.slave_ids, rule.function_codes, rule.addresses):
            try:
                dup = rules[addr]
            except KeyError:
                rules[addr] = endpoint
            else:
                conflicts = [f'{summary.filename}:{summary.lineno} ({summary.line!r})'
                             for summary in [endpoint.__self__.frame, dup.__self__.frame]]  # type: ignore[attr-defined]
                raise AssertionError(f'address {addr[-1]} at {conflicts[0]} duplicates '
                                     f'register at {conflicts[1]}')



class RequestHandler(tcp.RequestHandler):
    @no_type_check
    def process(self, request_adu: Any) -> Any:
        _local.values = {}
        _local.writes = {}
        try:
            return super().process(request_adu)
        finally:
            for reg, value in _local.writes.items():
                try:
                    reg.fset(value)
                except Exception:
                    summary = set.__self__.frame
                    _log.exception(f'an unhandled exception occurred while setting a register defined at {summary.filename}:{summary.lineno}')
            del _local.values
            del _local.writes


def tcp_app(*args: Any, slave_id: int = 1, byteorder: str = 'big',
            mixed: bool = False, default_port: int = 502,
            **kwargs: Any) -> Callable[[_FN], Callable[[], None]]:
    """Decorator to handle boilerplate code for a TCP Modbus server

    Use this decorator to easily create a Modbus slave application. The
    decorated function must return a context manager. When entered, it
    should perform any initialization and then setup the Modbus routing.
    On exit, it should perform any cleanup, like closing file handles.
    The function can be decorated with additional click options that
    will be passed on to the function along with the server instance (as
    the first parameter).
    """
    import click

    def wrapper(setup: Callable[..., ContextManager]) -> Callable[[], None]:
        @click.command(*args, **kwargs)
        @click.help_option(help='show this message and exit')
        @click.option('-a', '--address', type=ipaddress.ip_address, default='::')
        @click.option('-p', '--port', type=click.IntRange(0, 65535), default=default_port)
        @click.option('--reuse-addr/--no-reuse-addr', default=True,
                      help='reuse IP address and port')
        @functools.wraps(setup)
        def tcp_loop(address: str, port: int, reuse_addr: bool, **kwargs: Any) -> None:
            StreamServer.reuse_addr = reuse_addr
            # The ellipsis is used for the handler here as the *real*
            # handler will be set below.
            server: StreamServer = patch_server(
                tcp.get_server(StreamServer, (str(address), port), ...),
                slave_id=slave_id, byteorder=byteorder, mixed=mixed)

            # gevent's StreamServer doesn't pass the server to the handler,
            # so umodbus's RequestHandler must be wrapped in a function that
            # adds the server to the arguments.
            server.set_handle(functools.partial(RequestHandler, server=server))

            with contextlib.closing(server), setup(server, **kwargs):
                assert_unique_addresses(server)
                server.serve_forever()
        return tcp_loop
    return wrapper
