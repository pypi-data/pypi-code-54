""" Tools for programatically working with numpy-style docstrings in python

See Also
--------
https://numpydoc.readthedocs.io/en/latest/format.html
"""

from .ast_tools import documentable_node_at_point

from .docstring_tools import Docstring

from .application import check, fix, fill_missing, check_missing

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "develop"

__all__ = [
    '__version__',
    'Docstring',
    'check',
    'check_missing',
    'documentable_node_at_point',
    'fill_missing',
    'fix',
]
