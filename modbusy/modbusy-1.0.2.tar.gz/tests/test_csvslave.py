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

from io import StringIO

import modbusy
import pytest
import voluptuous

from modbusy import csvslave
from modbusy.csvslave import _data_loop, _string, get_parser, validate


def test_data_loop():
    with StringIO('a,b,c\n1,2,3\n4,5,6\n') as file:
        loop = _data_loop(file, None, 0)
        for i in range(10):
            assert next(loop) == (['a', 'b', 'c'], 1)
            assert next(loop) == (['1', '2', '3'], 2)
            assert next(loop) == (['4', '5', '6'], 3)
        loop = _data_loop(file, None, 1)
        for i in range(10):
            assert next(loop) == (['1', '2', '3'], 2)
            assert next(loop) == (['4', '5', '6'], 3)


def test_string_parser():
    assert _string('abcd') == b'abcd'
    assert _string(1234) == b'1234'
    assert _string(True) == b'True'
    assert _string(1234.5678) == b'1234.5678'


def test_get_parser():
    assert get_parser(modbusy.BOOL) == csvslave._parse_functions[modbusy.Boolean]
    assert get_parser(modbusy.FLOAT) == float
    assert get_parser(modbusy.DOUBLE) == float
    assert get_parser(modbusy.INT16) == int
    assert get_parser(modbusy.INT32) == int
    assert get_parser(modbusy.INT64) == int
    assert get_parser(modbusy.INT128) == int
    assert get_parser(modbusy.UINT16) == int
    assert get_parser(modbusy.UINT32) == int
    assert get_parser(modbusy.UINT64) == int
    assert get_parser(modbusy.UINT128) == int
    assert get_parser(modbusy.String(8)) == _string
    assert get_parser(modbusy.String(16)) == _string
    with pytest.raises(AssertionError, match='failed to find a parser'):
        get_parser(int)


@pytest.fixture
def config():
    return {'registers': [{'address': 0, 'trigger': True}]}

def register(config):
    return config['registers'][0]

def default(config={}, register={}):
    reg = {
        'address': 0,
        'column': None,
        'value': 0,
        'type': modbusy.INT16,
        'trigger': True,
        'slave_id': None,
        'byteorder': None,
        'mixed': None,
    }
    reg.update(register)
    data = {
        'slave_id': 1,
        'byteorder': 'big',
        'mixed': False,
        'registers': [reg],
    }
    data.update(config)
    return data


def test_validate(config):
    with pytest.raises(voluptuous.MultipleInvalid, match='required key not provided'):
        validate({})
    with pytest.raises(voluptuous.MultipleInvalid, match='expected a dictionary'):
        validate([])
    validate({'registers': []})
    assert validate(config) == default()


def _test_slave_id(config, data, match):
    key = 'config' if config is data else 'register'
    slave_id = lambda value: default(**{key: dict(slave_id=value)})
    data['slave_id'] = 0
    with pytest.raises(voluptuous.MultipleInvalid, match=match):
        validate(config)
    data['slave_id'] = 1
    assert validate(config) == slave_id(1)
    data['slave_id'] = 255
    assert validate(config) == slave_id(255)
    data['slave_id'] = 256
    with pytest.raises(voluptuous.MultipleInvalid, match=match):
        validate(config)

def test_validate_slave_id(config):
    config['slave_id'] = None
    with pytest.raises(voluptuous.MultipleInvalid, match='expected int'):
        validate(config)
    _test_slave_id(config, config, 'value must be at (least 1|most 255)')

def test_validate_register_slave_id(config):
    data = register(config)
    data['slave_id'] = None
    assert validate(config) == default(register=dict(slave_id=None))
    _test_slave_id(config, data, 'not a valid value')


def _test_byte_order(config, data):
    key = 'config' if config is data else 'register'
    byteorder = lambda value: default(**{key: dict(byteorder=value)})
    data['byteorder'] = 'big'
    assert validate(config) == byteorder('big')
    data['byteorder'] = 'little'
    assert validate(config) == byteorder('little')
    data['byteorder'] = 'any'
    with pytest.raises(voluptuous.MultipleInvalid, match='value is not allowed'):
        validate(config)

def test_validate_byteorder(config):
    config['byteorder'] = None
    with pytest.raises(voluptuous.MultipleInvalid, match='value is not allowed'):
        validate(config)
    _test_byte_order(config, config)

def test_register_validate_byteorder(config):
    data = register(config)
    data['byteorder'] = None
    assert validate(config)
    _test_byte_order(config, data)


def _test_mixed(config, data, match):
    key = 'config' if config is data else 'register'
    true = default(**{key: dict(mixed=True)})
    false = default(**{key: dict(mixed=False)})
    data['mixed'] = True
    assert validate(config) == true
    data['mixed'] = False
    assert validate(config) == false
    data['mixed'] = 1
    assert validate(config) == true
    data['mixed'] = 0
    assert validate(config) == false
    data['mixed'] = 'yes'
    assert validate(config) == true
    data['mixed'] = 'no'
    assert validate(config) == false
    data['mixed'] = ''
    with pytest.raises(voluptuous.MultipleInvalid, match=match):
        validate(config)

def test_validate_mixed(config):
    config['mixed'] = None
    with pytest.raises(voluptuous.MultipleInvalid, match='not a valid value'):
        validate(config)
    _test_mixed(config, config, 'expected boolean')

def test_validate_register_mixed(config):
    data = register(config)
    data['mixed'] = None
    assert validate(config) == default(register=dict(mixed=None))
    _test_mixed(config, data, 'not a valid value')


def test_validate_register_address(config):
    data = register(config)
    address = lambda value: default(register=dict(address=value))
    data['address'] = -1
    with pytest.raises(voluptuous.MultipleInvalid, match='value must be at least 0'):
        validate(config)
    data['address'] = 0
    assert validate(config) == address(0)
    data['address'] = 65535
    assert validate(config) == address(65535)
    data['address'] = 65536
    with pytest.raises(voluptuous.MultipleInvalid, match='value must be at most 65535'):
        validate(config)
    data['address'] = [0, 2, 4]
    assert validate(config) == address([0, 2, 4])


def test_validate_register_column(config):
    data = register(config)
    column = lambda column, value=None: default(register=dict(column=column, value=value))
    data['column'] = None
    assert validate(config) == column(None, 0)
    data['column'] = -1
    assert validate(config) == column(-1)
    data['column'] = 0
    assert validate(config) == column(0)
    data['column'] = 65535
    assert validate(config) == column(65535)
    data['column'] = ''
    assert validate(config) == column('')
    data['column'] = 'abc'
    assert validate(config) == column('abc')
    data['column'] = 'xyz'
    assert validate(config) == column('xyz')
    data['column'] = 1.2
    with pytest.raises(voluptuous.MultipleInvalid, match='not a valid value'):
        validate(config)


def test_validate_register_value(config):
    data = register(config)
    for data['type'], kind, valid, invalid in [
                ('bool', modbusy.BOOL,
                 [True, False, ('yes', True), ('no', False),
                  ('true', True), ('false', False), (1, True), (0, False),
                  (1.3, True), (0.0, False), (None, False)],
                 ['', 'affirmative', 'negative']),
                *((name, getattr(modbusy, name.upper()),
                   [0.0, -1.1, 3.14159, 1.2e-10, 0, 4, -3, ('10.2', 10.2), ('2', 2.0)],
                   ['abc', '', '0xabcd']) for name in ['double', 'float']),
                *((name, getattr(modbusy, name.upper()),
                  [0, -3, 9, -127, 128, (1.3, 1), 65535],
                  ['0xabcd', '0o456']) for name in['int16', 'int32', 'int64', 'int128',
                                                   'uint16', 'uint32', 'uint64', 'uint128']),
                *((f'string[{i}]', modbusy.String(i),
                   [('', b''), (None, b''), ('abcd', b'abcd'), (1.23, b'1.23'), (True, b'True')],
                   []) for i in [1, 2, 20, 2000]),
            ]:
        for test in valid:
            if isinstance(test, tuple):
                data['value'], expected = test
            else:
                data['value'] = expected = test
            assert validate(config) == default(register=dict(type=kind, value=expected))
        for data['value'] in invalid:
            with pytest.raises(voluptuous.MultipleInvalid, match='value is not of the given type|not a valid value'):
                validate(config)


def test_validate_register_type(config):
    data = register(config)
    for data['type'], kind, value in [
                ('bool', modbusy.BOOL, False),
                ('double', modbusy.DOUBLE, 0.0),
                ('float', modbusy.FLOAT, 0.0),
                ('int16', modbusy.INT16, 0),
                ('int32', modbusy.INT32, 0),
                ('int64', modbusy.INT64, 0),
                ('int128', modbusy.INT128, 0),
                ('string[1]', modbusy.String(1), b''),
                ('string[2]', modbusy.String(2), b''),
                ('string[20]', modbusy.String(20), b''),
                ('string[2000]', modbusy.String(2000), b''),
            ]:
        assert validate(config) == default(register=dict(type=kind, value=value))
    for data['type'] in [None, '', 'int3', 'string[0]', 'string[-10]']:
        with pytest.raises(voluptuous.MultipleInvalid, match='invalid register type|not a valid value'):
            validate(config)


def test_validate_register_trigger(config):
    data = register(config)
    true = default()
    extra = register(default(register=dict(address=1)))
    true['registers'].append(extra)
    false = default(register=dict(trigger=False))
    false['registers'].append(extra)
    data['trigger'] = None
    validate(config)
    config['registers'].append({'address': 1, 'trigger': True})
    data['trigger'] = True
    assert validate(config) == true
    data['trigger'] = False
    assert validate(config) == false
    data['trigger'] = 1
    assert validate(config) == true
    data['trigger'] = 0
    assert validate(config) == false
    data['trigger'] = 'yes'
    assert validate(config) == true
    data['trigger'] = 'no'
    assert validate(config) == false
    data['trigger'] = ''
    with pytest.raises(voluptuous.MultipleInvalid, match='expected boolean'):
        validate(config)
    data['trigger'] = None
    assert validate(config) == false
