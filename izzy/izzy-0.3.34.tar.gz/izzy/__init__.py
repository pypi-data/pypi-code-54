
from . import datasets
from . import framework

from .classification import *
from .datasets import *
from .defaults import *
from .eda import *
from .features import *
from .framework import *
from .io import *
from .misc import *
from .regression import *
from .tests import *
from .version import __version__
from .viz import *

# TODO pandas.modin for speedup? Make this an option
__all__ = []
__all__.extend(datasets.__all__)
__all__.extend(framework.__all__)
