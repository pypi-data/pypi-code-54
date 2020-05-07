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

import contextlib
from types import MethodType

import pytest

from umodbus.functions import (READ_COILS, READ_DISCRETE_INPUTS, WRITE_MULTIPLE_COILS,
                               WRITE_SINGLE_COIL, READ_HOLDING_REGISTERS, READ_INPUT_REGISTERS,
                               WRITE_MULTIPLE_REGISTERS, WRITE_SINGLE_REGISTER)
from umodbus.route import Map
from umodbus.server import route

import modbusy


class MockServer:
    def __init__(self, **kwargs):
        self.route_map = Map()
        self.route = MethodType(route, self)
        modbusy.patch_server(self, **kwargs)


@pytest.fixture
def server():
    return MockServer()


@contextlib.contextmanager
def adu():
    modbusy._local.values = {}
    modbusy._local.writes = {}
    try:
        yield
    finally:
        for reg, value in modbusy._local.writes.items():
            reg.fset(value)
        del modbusy._local.values
        del modbusy._local.writes


def _test_read(server, function_code, address, expected_value, slave_id=1):
    kwargs = dict(slave_id=slave_id, function_code=function_code, address=address)
    endpoint = server.route_map.match(**kwargs)
    if expected_value is None:
        assert endpoint is None
    else:
        assert endpoint is not None
        with adu():
            value = endpoint(**kwargs)
        #assert hex(word) == hex(expected_word)  # Human form
        assert value == expected_value


def _test_write(server, function_code, address, value, slave_id=1):
    kwargs = dict(slave_id=slave_id, function_code=function_code, address=address)
    endpoint = server.route_map.match(**kwargs)
    assert endpoint is not None
    with adu():
        endpoint(value=value, **kwargs)
    read_code = {
        WRITE_SINGLE_COIL: READ_COILS,
        WRITE_MULTIPLE_COILS: READ_COILS,
        WRITE_SINGLE_REGISTER: READ_HOLDING_REGISTERS,
        WRITE_MULTIPLE_REGISTERS: READ_HOLDING_REGISTERS,
    }[function_code]
    _test_read(server, read_code, address, value)


def _register_id(register):
    kind, value, _, byteorder, mixed = register
    try:
        sign = '-' if value < 0 else ''
    except TypeError:
        sign = ''
    return f'{sign}{kind}.{byteorder}{".mixed" if mixed else ""}'


@pytest.fixture(params=[
    ('UINT16', 0x0a0b, [0x0a0b], 'big', False),
    ('UINT16', 0x0a0b, [0x0a0b], 'big', True),
    ('UINT16', 0x0a0b, [0x0b0a], 'little', False),
    ('UINT16', 0x0a0b, [0x0b0a], 'little', True),

    ('UINT32', 0x0a0b0c0d, [0x0a0b, 0x0c0d], 'big', False),
    ('UINT32', 0x0a0b0c0d, [0x0b0a, 0x0d0c], 'big', True),
    ('UINT32', 0x0a0b0c0d, [0x0d0c, 0x0b0a], 'little', False),
    ('UINT32', 0x0a0b0c0d, [0x0c0d, 0x0a0b], 'little', True),

    ('UINT64', 0x0a0b0c0d01020304, [0x0a0b, 0x0c0d, 0x0102, 0x0304], 'big', False),
    ('UINT64', 0x0a0b0c0d01020304, [0x0b0a, 0x0d0c, 0x0201, 0x0403], 'big', True),
    ('UINT64', 0x0a0b0c0d01020304, [0x0403, 0x0201, 0x0d0c, 0x0b0a], 'little', False),
    ('UINT64', 0x0a0b0c0d01020304, [0x0304, 0x0102, 0x0c0d, 0x0a0b], 'little', True),

    ('INT16', 0x0a0b, [0x0a0b], 'big', False),
    ('INT16', 0x0a0b, [0x0a0b], 'big', True),
    ('INT16', 0x0a0b, [0x0b0a], 'little', False),
    ('INT16', 0x0a0b, [0x0b0a], 'little', True),

    ('INT16', -0x0a0b, [0xf5f5], 'big', False),
    ('INT16', -0x0a0b, [0xf5f5], 'big', True),
    ('INT16', -0x0a0b, [0xf5f5], 'little', False),
    ('INT16', -0x0a0b, [0xf5f5], 'little', True),

    ('INT32', 0x0a0b0c0d, [0x0a0b, 0x0c0d], 'big', False),
    ('INT32', 0x0a0b0c0d, [0x0b0a, 0x0d0c], 'big', True),
    ('INT32', 0x0a0b0c0d, [0x0d0c, 0x0b0a], 'little', False),
    ('INT32', 0x0a0b0c0d, [0x0c0d, 0x0a0b], 'little', True),

    ('INT32', -0x0a0b0c0d, [0xf5f4, 0xf3f3], 'big', False),
    ('INT32', -0x0a0b0c0d, [0xf4f5, 0xf3f3], 'big', True),
    ('INT32', -0x0a0b0c0d, [0xf3f3, 0xf4f5], 'little', False),
    ('INT32', -0x0a0b0c0d, [0xf3f3, 0xf5f4], 'little', True),

    ('INT64', 0x0a0b0c0d01020304, [0x0a0b, 0x0c0d, 0x0102, 0x0304], 'big', False),
    ('INT64', 0x0a0b0c0d01020304, [0x0b0a, 0x0d0c, 0x0201, 0x0403], 'big', True),
    ('INT64', 0x0a0b0c0d01020304, [0x0403, 0x0201, 0x0d0c, 0x0b0a], 'little', False),
    ('INT64', 0x0a0b0c0d01020304, [0x0304, 0x0102, 0x0c0d, 0x0a0b], 'little', True),

    ('INT64', -0x0a0b0c0d01020304, [0xf5f4, 0xf3f2, 0xfefd, 0xfcfc], 'big', False),
    ('INT64', -0x0a0b0c0d01020304, [0xf4f5, 0xf2f3, 0xfdfe, 0xfcfc], 'big', True),
    ('INT64', -0x0a0b0c0d01020304, [0xfcfc, 0xfdfe, 0xf2f3, 0xf4f5], 'little', False),
    ('INT64', -0x0a0b0c0d01020304, [0xfcfc, 0xfefd, 0xf3f2, 0xf5f4], 'little', True),

    ('FLOAT', 6.694873056790824e-33, [0x0a0b, 0x0c0d], 'big', False),
    ('FLOAT', 6.694873056790824e-33, [0x0b0a, 0x0d0c], 'big', True),
    ('FLOAT', 6.694873056790824e-33, [0x0d0c, 0x0b0a], 'little', False),
    ('FLOAT', 6.694873056790824e-33, [0x0c0d, 0x0a0b], 'little', True),

    ('FLOAT', -6.694873056790824e-33, [0x8a0b, 0x0c0d], 'big', False),
    ('FLOAT', -6.694873056790824e-33, [0x0b8a, 0x0d0c], 'big', True),
    ('FLOAT', -6.694873056790824e-33, [0x0d0c, 0x0b8a], 'little', False),
    ('FLOAT', -6.694873056790824e-33, [0x0c0d, 0x8a0b], 'little', True),

    ('DOUBLE', 2.7486158043386135e-260, [0x0a0b, 0x0c0d, 0x0102, 0x0304], 'big', False),
    ('DOUBLE', 2.7486158043386135e-260, [0x0b0a, 0x0d0c, 0x0201, 0x0403], 'big', True),
    ('DOUBLE', 2.7486158043386135e-260, [0x0403, 0x0201, 0x0d0c, 0x0b0a], 'little', False),
    ('DOUBLE', 2.7486158043386135e-260, [0x0304, 0x0102, 0x0c0d, 0x0a0b], 'little', True),

    ('DOUBLE', -2.7486158043386135e-260, [0x8a0b, 0x0c0d, 0x0102, 0x0304], 'big', False),
    ('DOUBLE', -2.7486158043386135e-260, [0x0b8a, 0x0d0c, 0x0201, 0x0403], 'big', True),
    ('DOUBLE', -2.7486158043386135e-260, [0x0403, 0x0201, 0x0d0c, 0x0b8a], 'little', False),
    ('DOUBLE', -2.7486158043386135e-260, [0x0304, 0x0102, 0x0c0d, 0x8a0b], 'little', True),

    (modbusy.String(4), b'abcd', [0x6162, 0x6364], 'big', False),
    (modbusy.String(4), b'abcd', [0x6261, 0x6463], 'big', True),
    # Strings are always in big-endian byte order
    (modbusy.String(4), b'abcd', [0x6162, 0x6364], 'little', False),
    (modbusy.String(4), b'abcd', [0x6261, 0x6463], 'little', True),

    (modbusy.String(5), b'abcde', [0x6162, 0x6364, 0x6500], 'big', False),
    (modbusy.String(5), b'abcde', [0x6261, 0x6463, 0x0065], 'big', True),
    # Strings are always in big-endian byte order
    (modbusy.String(5), b'abcde', [0x6162, 0x6364, 0x6500], 'little', False),
    (modbusy.String(5), b'abcde', [0x6261, 0x6463, 0x0065], 'little', True),
], ids=_register_id)
def register(request):
    return request.param


def test_input_register(server, register):
    kind, value, words, byteorder, mixed = register
    if isinstance(kind, str):
        kind = getattr(modbusy, kind)

    @server.register(0, kind, byteorder=byteorder, mixed=mixed)
    def get(for_write):
        return value

    for address, expected_word in enumerate(words + [None]):
        _test_read(server, READ_INPUT_REGISTERS, address, expected_word)
    for function_code in [READ_COILS, READ_HOLDING_REGISTERS, READ_DISCRETE_INPUTS,
                          WRITE_MULTIPLE_COILS, WRITE_MULTIPLE_COILS,
                          WRITE_MULTIPLE_REGISTERS, WRITE_SINGLE_REGISTER]:
        endpoint = server.route_map.match(slave_id=1, function_code=function_code, address=0)
        assert endpoint is None



def test_holding_register(server, register):
    kind, value, words, byteorder, mixed = register
    if isinstance(kind, str):
        kind = getattr(modbusy, kind)

    @server.register(0, kind, byteorder=byteorder, mixed=mixed)
    def get(for_write):
        return value

    @get.setter
    def set(new_value):
        nonlocal value
        value = new_value

    for address, expected_word in enumerate(words + [None]):
        _test_read(server, READ_HOLDING_REGISTERS, address, expected_word)
        if expected_word is not None:
            test_word = expected_word ^ (0xffffffffffffffff >> (8 - kind.count) * 16)
            _test_write(server, WRITE_SINGLE_REGISTER, address, test_word)
            _test_write(server, WRITE_MULTIPLE_REGISTERS, address, expected_word)
    for function_code in [READ_COILS, READ_INPUT_REGISTERS, READ_DISCRETE_INPUTS,
                          WRITE_MULTIPLE_COILS, WRITE_MULTIPLE_COILS]:
        endpoint = server.route_map.match(slave_id=1, function_code=function_code, address=0)
        assert endpoint is None


@pytest.fixture(params=[True, False])
def boolean(request):
    return request.param


def test_discrete_input(server, boolean):
    @server.register(0, modbusy.BOOL)
    def get(for_write):
        return boolean

    for address, expected_value in enumerate([boolean, None]):
        _test_read(server, READ_DISCRETE_INPUTS, address, expected_value)
    for function_code in [READ_COILS, READ_HOLDING_REGISTERS, READ_INPUT_REGISTERS,
                          WRITE_MULTIPLE_COILS, WRITE_MULTIPLE_COILS,
                          WRITE_MULTIPLE_REGISTERS, WRITE_SINGLE_REGISTER]:
        endpoint = server.route_map.match(slave_id=1, function_code=function_code, address=0)
        assert endpoint is None


def test_coil(server, boolean):
    @server.register(0, modbusy.BOOL)
    def get(for_write):
        return boolean

    @get.setter
    def set(value):
        nonlocal boolean
        boolean = value

    for address, expected_value in enumerate([boolean, None]):
        _test_read(server, READ_COILS, address, expected_value)
        if expected_value is not None:
            _test_write(server, WRITE_SINGLE_COIL, address, not expected_value)
            _test_write(server, WRITE_MULTIPLE_COILS, address, expected_value)
    for function_code in [READ_DISCRETE_INPUTS, READ_HOLDING_REGISTERS, READ_INPUT_REGISTERS,
                          WRITE_MULTIPLE_REGISTERS, WRITE_SINGLE_REGISTER]:
        endpoint = server.route_map.match(slave_id=1, function_code=function_code, address=0)
        assert endpoint is None


def test_server_defaults():
    def get(for_write):
        return 0x0a0b0c0d

    def test_options(server_options=None, register_options=None):
        if server_options is None:
            server_options = {}
        if register_options is None:
            register_options = {}
        slave_id = register_options.get('slave_id', server_options.get('slave_id', 1))
        kwargs = dict(slave_id=slave_id, function_code=READ_INPUT_REGISTERS, address=0)
        server = MockServer(**server_options)
        server.register(0, modbusy.UINT32, **register_options)(get)
        endpoint = server.route_map.match(**kwargs)
        assert endpoint is not None
        with adu():
            return (*server._default_options, slave_id, endpoint(**kwargs))

    _ = dict
    assert test_options() == (1, 'big', False, 1, 0x0a0b)
    assert test_options(_(slave_id=2)) == (2, 'big', False, 2, 0x0a0b)
    assert test_options(_(byteorder='little')) == (1, 'little', False, 1, 0x0d0c)
    assert test_options(_(mixed=True)) == (1, 'big', True, 1, 0x0b0a)
    assert test_options(None, _(slave_id=2)) == (1, 'big', False, 2, 0x0a0b)
    assert test_options(_(slave_id=2), _(slave_id=1)) == (2, 'big', False, 1, 0x0a0b)
    assert test_options(None, _(byteorder='little')) == (1, 'big', False, 1, 0x0d0c)
    assert test_options(_(byteorder='little'), _(byteorder='big')) == (1, 'little', False, 1, 0x0a0b)
    assert test_options(None, _(mixed=True)) == (1, 'big', False, 1, 0x0b0a)
    assert test_options(_(mixed=True), _(mixed=False)) == (1, 'big', True, 1, 0x0a0b)


def test_trigger(server):
    read_count = 0
    write_count = 0

    @server.register(100, modbusy.UINT32)
    def get(for_write):
        nonlocal read_count
        read_count += not for_write
        return 0

    @get.setter
    def set(value):
        nonlocal read_count, write_count
        write_count += 1

    with adu():
        for address in 100, 101:
            kwargs = dict(slave_id=1, function_code=READ_HOLDING_REGISTERS, address=address)
            server.route_map.match(**kwargs)(**kwargs)
            kwargs = dict(slave_id=1, function_code=WRITE_SINGLE_REGISTER, address=address)
            server.route_map.match(**kwargs)(**kwargs, value=0)

    assert read_count == 1
    assert write_count == 1


def test_attribute(server):
    class Object:
        a = 0x0a0b0c0d
        def __init__(self):
            self.b = 0x01020304
    obj = Object()

    server.register(200, modbusy.UINT32).attribute(Object, 'a')
    server.register(250, modbusy.UINT32).attribute(Object, 'a', writable=False)
    server.register(300, modbusy.UINT32).attribute(obj, 'b')

    _test_read(server, READ_HOLDING_REGISTERS, 200, 0x0a0b)
    _test_write(server, WRITE_MULTIPLE_REGISTERS, 201, 0)
    _test_read(server, READ_INPUT_REGISTERS, 250, 0x0a0b)
    _test_read(server, READ_HOLDING_REGISTERS, 301, 0x0304)
    _test_write(server, WRITE_MULTIPLE_REGISTERS, 300, 0)

    assert Object.a == 0x0a0b0000
    assert obj.b == 0x0304


def test_assert_unique_addresses(server):
    @server.register(100, modbusy.BOOL)
    def foo(for_write):
        return True
    modbusy.assert_unique_addresses(server)

    @server.register(100, modbusy.BOOL)
    def bar(for_write):
        return True
    with pytest.raises(AssertionError):
        modbusy.assert_unique_addresses(server)


def test_validate_slave_id():
    with pytest.raises(ValueError):
        modbusy._validate_slave_id(0)
    modbusy._validate_slave_id(1)
    modbusy._validate_slave_id(255)
    with pytest.raises(ValueError):
        modbusy._validate_slave_id(256)


def test_validate_byteorder():
    with pytest.raises(ValueError):
        modbusy._validate_byteorder('')
    modbusy._validate_byteorder('big')
    modbusy._validate_byteorder('little')
    with pytest.raises(ValueError):
        modbusy._validate_byteorder('mixed')


def test_validate_address():
    with pytest.raises(ValueError):
        modbusy._validate_address(-1)
    modbusy._validate_address(0)
    modbusy._validate_address(65535)
    with pytest.raises(ValueError):
        modbusy._validate_address(65536)


def test_invalid_register_init(server):
    with pytest.raises(TypeError):
        server.register()
    with pytest.raises(TypeError):
        server.register(0)
    with pytest.raises(ValueError):
        server.register(0, modbusy.UINT16, slave_id=0)
    with pytest.raises(ValueError):
        server.register(0, modbusy.UINT16, slave_id=256)
    with pytest.raises(ValueError):
        server.register(0, modbusy.UINT16, byteorder='')
    with pytest.raises(ValueError):
        server.register(0, modbusy.UINT16, byteorder='other')


def test_invalid_server_init():
    with pytest.raises(ValueError):
        MockServer(slave_id=0)
    with pytest.raises(ValueError):
        MockServer(slave_id=256)
    with pytest.raises(ValueError):
        MockServer(byteorder='')
    with pytest.raises(ValueError):
        MockServer(byteorder='other')
