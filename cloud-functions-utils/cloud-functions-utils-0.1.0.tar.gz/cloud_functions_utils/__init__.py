"""
Helper functions for Google Cloud Services.
"""

from itertools import islice
import re


def chunks(iterable, chunksize=500):
    iterable = iter(iterable)
    while True:
        chunk = tuple(islice(iterable, chunksize))
        if not chunk:
            return
        yield chunk


def camel_to_snake(term):
    """
    Converts a CamedCased term into a snake_cased term.
    """
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", term).lower()
