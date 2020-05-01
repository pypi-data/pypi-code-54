from functools import wraps
from typing import Callable, Iterator, List, Tuple, TypeVar

T = TypeVar("T")


def n_grams(it: Iterator[T], n: int) -> Iterator[Tuple[T, ...]]:
    """
    Computes all n-grams from an iterator. By example:

    >>> assert list(n_grams([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]
    """

    stack = []

    for i in it:
        stack.append(i)

        if len(stack) > n:
            stack.pop(0)

        if len(stack) == n:
            yield tuple(stack)


def return_list(f: Callable[..., Iterator[T]]) -> Callable[..., List[T]]:
    """
    Decorator that converts any iterator-returning function into a
    list-returning function.

    Typically useful for generators that are expected to return a list.
    """

    @wraps(f)
    def wrapper(*args, **kwargs) -> List[T]:
        return list(f(*args, **kwargs))

    return wrapper
