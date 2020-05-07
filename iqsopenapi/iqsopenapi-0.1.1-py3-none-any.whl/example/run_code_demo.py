# -*- coding: utf-8 -*-

from iqsopenapi import *

code = """
from iqsopenapi import *


def init(context):
    logger.info("init")
    context.s1 = "rb2010.SHFE"


def handle_tick(context, tick):
    logger.info('tick:{0},{1},{2}'.format(tick.Symbol,tick.LocalTime,tick.LastPx))
"""

config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
      "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": False
    }
  }
}

run_code(code,config)