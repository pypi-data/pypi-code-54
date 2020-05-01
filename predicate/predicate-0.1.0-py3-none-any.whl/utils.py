from copy import deepcopy
from functools import reduce, wraps
from typing import Any, Callable, Iterable, List, Optional, TypeVar

A = TypeVar('A')
B = TypeVar('B')


def flip(func) -> Callable:
    @wraps(func)
    def flipped(*args):
        return func(*reversed(args))

    return flipped


def identity(a: A) -> A:
    return a


def apply_to(value: A, func: Callable[[A], B]) -> B:
    return func(value)


def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, identity)


def contains(haystack: Iterable[A], needle: A) -> bool:
    return needle in haystack


def startswith(target: str, start: str) -> bool:
    return target.startswith(start)


def endswith(target: str, end: str) -> bool:
    return target.endswith(end)


def iexact(a: str, b: str) -> bool:
    return a.lower() == b.lower()


def _safe_lens(path: List[str]) -> Callable[[Any], Optional[Any]]:
    """
    Digs into nested structures defaulting to None

    >>> _safe_lens(['foo'])({'foo': 'bar'})
    'bar'
    >>> _safe_lens(['foo', 'bar'])({'foo': {'bar': 'baz'}})
    'baz'
    >>> _safe_lens(['foo', 'bar'])({'foo': 'bar'})

    """

    def lens(target):
        _data = deepcopy(target)
        keypath = path[:]
        while keypath and _data is not None:
            k = keypath.pop(0)
            if isinstance(_data, dict):
                _data = _data.get(str(k), None)
            else:
                _data = getattr(_data, str(k), None)
        return _data

    return lens
