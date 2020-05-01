from functools import partial
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, TypeVar

from .comparator import COMPARATORS, Comparator, comparator_from_string
from .utils import _safe_lens, compose, flip

A = TypeVar('A')
B = TypeVar('B')

Predicate = Callable[[A], bool]


def process_kwargs(key_word_arguments_dict: Dict[str, Any]) -> Iterable[Predicate]:
    """
    Transform the Dictionary of Key Word arguments into a iterable of predicate functions
    """
    return map(_process_predicate, key_word_arguments_dict.items())


def _process_predicate(predicate_pair: Tuple[str, Any]) -> Predicate:
    """
    Take a field and a value and return a predicate function
    """
    predicate_field, value = predicate_pair
    attribute_accessor, comparator = _process_predicate_field(predicate_field)
    return compose(partial(flip(COMPARATORS[comparator]), value), attribute_accessor)


def _process_predicate_field(field: str) -> Tuple[Callable[[Any], Optional[Any]], Comparator]:
    """
    breaks down the first part of the kwargs into a nested attribute accessor and a comparison function defaulting to eq

    >>> getter, comparator = _process_predicate_field('name')
    >>> getter({'name': 'bob'})
    'bob'
    >>> comparator == Comparator.EQ
    True
    >>> getter, comparator = _process_predicate_field('name__first__iexact')
    >>> getter({'name': {'first': 'Joe'}})
    'Joe'
    >>> comparator == Comparator.IEXACT
    True

    """
    parts = field.split("__")
    *init, last = parts
    maybe_comparator = comparator_from_string(last)
    if maybe_comparator is not None:
        return _safe_lens(init), maybe_comparator
    return _safe_lens(parts), Comparator.EQ
