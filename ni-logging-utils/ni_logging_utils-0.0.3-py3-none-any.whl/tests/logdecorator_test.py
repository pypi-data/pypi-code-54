import logging

from pytest import raises

from logging_utils import LogDecorator

from .context import logging_utils


@LogDecorator(decorator_log='inspect-fun', resume=True)
def fun(value):
    return value


@LogDecorator(decorator_log='inspect-fun')
def fun2(value, virtual=False):
    return value


@LogDecorator(decorator_log='inspect-fun')
def fun3():
    raise TypeError('should have a value')


def test_should_return_array_or_size(caplog):
    caplog.set_level(logging.DEBUG)

    fun(['a', 'b', 'c'])
    assert len(caplog.records) == 2
    assert caplog.records[0].getMessage() == "fun - (['a', 'b', 'c'],) - {}"
    assert caplog.records[0].levelno == logging.DEBUG

    assert caplog.records[1].getMessage() == "Function return 3 values"
    assert caplog.records[1].levelno == logging.DEBUG

    caplog.clear()

    fun2(['a', 'b', 'c'], virtual=True)
    assert len(caplog.records) == 2
    assert caplog.records[0].getMessage() == "fun2 - (['a', 'b', 'c'],) - {'virtual': True}"
    assert caplog.records[0].levelno == logging.DEBUG

    assert caplog.records[1].getMessage() == "Function return ['a', 'b', 'c']"
    assert caplog.records[1].levelno == logging.DEBUG


def test_should_return_string(caplog):
    caplog.set_level(logging.DEBUG)
    fun2('test', virtual=True)
    assert len(caplog.records) == 2
    assert caplog.records[0].getMessage() == "fun2 - ('test',) - {'virtual': True}"
    assert caplog.records[0].levelno == logging.DEBUG

    assert caplog.records[1].getMessage() == "Function return test"
    assert caplog.records[1].levelno == logging.DEBUG

    caplog.clear()

    fun('test')
    assert len(caplog.records) == 2
    assert caplog.records[0].getMessage() == "fun - ('test',) - {}"
    assert caplog.records[0].levelno == logging.DEBUG

    assert caplog.records[1].getMessage() == "Function return test"
    assert caplog.records[1].levelno == logging.DEBUG


def test_should_raise_exception():
    with raises(TypeError):
        fun3()
