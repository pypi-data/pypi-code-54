__version__ = '1.0.3'

import sys
if sys.platform != 'win32':
    raise Exception('xingapi requires 32bit working environment')

from xingapi.api.res import Res
from xingapi.api.xasession import Session
from xingapi.api.xaquery import Query
from xingapi.api.xareal import Real, RealManager