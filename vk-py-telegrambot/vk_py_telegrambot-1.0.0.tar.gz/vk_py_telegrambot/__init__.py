import logging
import os
import re
import sys
import time


logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)

console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)

from vk_py_telegrambot import bot
