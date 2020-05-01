__version__ = '0.1.0'

from typing import Any, Callable

from .process_kwargs import process_kwargs


def where(**kwargs) -> Callable[[Any], bool]:
    combinator = kwargs.pop('combinator', 'and')
    predicates = list(process_kwargs(kwargs))
    if combinator == 'and':
        return lambda x: all(func(x) for func in predicates)
    if combinator == 'or':
        return lambda x: any(func(x) for func in predicates)
    if combinator == 'none':
        return lambda x: not any(func(x) for func in predicates)
    if callable(combinator):
        return lambda x: combinator(func(x) for func in predicates)
    raise ValueError(f'{combinator} is not a valid argument for combinator.')
