"""Module-level docstring

This python module is a test fixture used by a number of static tests.
Avoid editing it!
"""
from __future__ import annotations

# just a comment. good documentation practices are important!

import asyncio
from dataclasses import dataclass
import typing as T


_MY_CONSTANT = "a very important string"

# Meaning of life, the universe, everything
_MY_DOCUMENTED_CONSTANT = 42  # type: int


class MyClass:
    """Here's a docstring for my class!

    Parameters
    ----------
    instance_variable
    is_cool : bool, optional

    Attributes
    ----------
    class_variable
    annotated_class_variable : str
    class_variable_without_assignment : T.Any
    data_structure
    is_cool : bool
        Docstring for a very cool property

    See Also
    --------
    ``MyDataclass`` : maybe this is related...
    """
    class_variable = 1969
    annotated_class_variable: str = f"{class_variable} in the sunshine"
    class_variable_without_assignment: T.Any

    data_structure = [8, 6, 7]  # type: T.List[int]
    data_structure[3] = 5

    def __init__(self, instance_variable, is_cool: bool = True):
        """<TODO summary>

        Parameters
        ----------
        instance_variable
        is_cool : bool, optional
        """
        self.instance_variable = instance_variable
        self._is_cool = is_cool

    def my_method(self, a: int, b: int) -> int:
        """This method adds two numbers, in a very regular sort of way

        Parameters
        ----------
        a : int
        b : int

        Returns
        -------
        int
        """
        return a + b

    @property
    def is_cool(self) -> bool:
        """Docstring for a very cool property"""
        return self._is_cool

    @is_cool.setter
    def is_cool(self, value: bool):
        """Docstring for a property setter?"""
        if value is False:
            raise ValueError("Sorry, I'm too cool for that")
        else:
            self._is_cool = value

    @classmethod
    def create_cool_instance(cls, instance_variable: T.Any) -> MyClass:
        """Here's a class method!

        It's probably a constructor.

        Parameters
        ----------
        instance_variable : T.Any

        Returns
        -------
        MyClass
        """
        return cls(instance_variable, is_cool=True)

    @staticmethod
    def _where_am_i(name: str):
        """<TODO summary>

        Parameters
        ----------
        name : str
        """
        print(f"You best start believin' in static methods, {name}... You're in one!")

    def _method_without_docstring(self, a: int, b: T.Optional[int]) -> None:
        """<TODO summary>

        Parameters
        ----------
        a : int
        b : int or None

        Returns
        -------
        None
        """
        def nested():
            return b, a


@dataclass
class _MyDataclass:
    """<TODO summary>

    Attributes
    ----------
    required : bool
    very_strange_type : iterable of int or T.Dict or bytes
    first : int
    second : float
    third : str
    fourth : list of int
    fifth : bytes
    sixth : bool
    seventh : dict of str, int
    """
    required: bool
    very_strange_type: T.Iterable[T.Union[int, T.Dict, bytes]]
    first: int = 8
    second: float = 6.0
    third: str = '7'
    fourth: T.List[int] = [5]
    fifth: bytes = b'\x03'
    sixth: bool = False
    seventh: T.Dict[str, int] = {'value': 9}

    def __str__(self):
        """<TODO summary>"""
        ret = type(self).__name__
        if self.is_cool:
            return f"COOL {ret}"
        else:
            return ret


def _my_function(
        a, b: int,
        c=8.0,  # type: float
        d: int = 6, *args, **kwargs):  # type: int
    """<TODO summary>

    Parameters
    ----------
    a
    b : int
    c : optional
    d : int, optional
    """
    return sum([
        a, b, c, d, *args, *kwargs.values()
    ])


def my_generator(value: str) -> T.Iterable[str]:
    """Docstring for my generator.

    Iterate through ``value``, disemvoweled.

    Parameters
    ----------
    value : str

    Yields
    ------
    iterable of str
    """

    for c in value:
        if c.lower() not in 'aeiou':
            yield c


def _my_better_generator(value: str) -> T.Iterable[str]:
    """<TODO summary>

    Parameters
    ----------
    value : str

    Returns
    -------
    iterable of str
    """
    yield from (c for c in value if c.lower() not in 'aeiou')


def _my_best_generator(value: str) -> T.Iterable[str]:
    """<TODO summary>

    Parameters
    ----------
    value : str

    Returns
    -------
    iterable of str
    """
    return (c for c in value if c.lower() not in 'aeiou')


async def my_coroutine(wait_time: int):
    """This docstring is for an `asyncio` coroutine!

    Parameters
    ----------
    wait_time : int
    """
    print("Help! I'm trapped in a")
    await asyncio.sleep(wait_time)
    print("`asyncio` coroutine!")


""" This is just a string somebody left in here.
It should be removed!
"""
