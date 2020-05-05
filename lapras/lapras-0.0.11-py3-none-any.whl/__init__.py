# coding:utf-8

from .detector import detect
from .stats import quality, IV, VIF, WOE
from .selection import select
from .transform import Combiner
from .metrics import KS, F1, PSI
from .plot import bin_plot,score_plot
from .model import Model
from .performance import performance
from .version import __version__

VERSION = __version__
