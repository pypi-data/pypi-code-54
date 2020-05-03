from typing import Callable, Generator, TypeVar
from operator import attrgetter as get_attr

SI = TypeVar('SI', str, int)


def filter_attr(generator: Generator, attr: str, op: Callable[[SI], bool], value: SI) -> Generator:
    """Returns a generator based on filter"""
    return (file for file in generator if op(get_attr(attr)(file if attr == "name" else file.stat()), value))
