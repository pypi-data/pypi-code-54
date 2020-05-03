import pkg_resources

from rockart_examples.exceptions import (
    RockartExamplesException,
    RockartExamplesIndexError,
    RockartExamplesValueError,
)


__all__ = [
    "RockartExamplesException",
    "RockartExamplesIndexError",
    "RockartExamplesValueError",
]

try:
    __version__ = pkg_resources.get_distribution("rockart-examples").version
except pkg_resources.DistributionNotFound:
    pass
