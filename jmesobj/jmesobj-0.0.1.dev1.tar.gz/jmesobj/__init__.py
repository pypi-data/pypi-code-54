import json

from dataclasses import dataclass
from typing import Dict

from jmespath import search

from .version import __version__  # noqa


@dataclass
class JMESObj:
    """JMESObj data container.

    Example:

    >>> obj = JMESObj({'foo': {'bar': True}})
    >>> obj['foo']
    {'bar': True}
    >>> obj['foo.bar']
    True
    >>> obj['foo.*']
    [True]

    >>> obj = JMESObj.from_json('{"foo": {"bar": true, "baz": false}}')
    >>> obj['foo.*']
    [True, False]

    """
    data: Dict

    @classmethod
    def from_json(cls, json_str: str):
        return cls(json.loads(json_str))

    def __getitem__(self, key):
        return search(key, self.data)
