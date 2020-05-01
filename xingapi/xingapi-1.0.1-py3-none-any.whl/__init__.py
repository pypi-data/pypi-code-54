__version__ = '1.0.1'

import sys
if sys.platform != 'win32':
    raise Exception('xingapi requires 32bit working environment')

from xingapi.res import Res
from xingapi.xasession import Session
from xingapi.xaquery import Query
from xingapi.xareal import Real, RealManager