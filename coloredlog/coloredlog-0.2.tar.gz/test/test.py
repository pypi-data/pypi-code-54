
import sys
sys.path.append('..')

import logging, coloredlog
logger = logging.getLogger(__name__)
logger.addHandler(coloredlog.ConsoleHandler())

logger.setLevel(logging.DEBUG)
logger.debug('debug')
logger.info('info')
logger.log(coloredlog.NOTIFY, 'notification')
logger.warning('warning')
logger.error('error')
try:
    raise RuntimeError('An exception!')
except:
    logger.exception('exception')
logger.critical('critical')


from coloredlog.color import *

print(deco('Hello, ', 0x011, bold=True) + reset() + 'world!')
print(deco('Hello, ', reverse=True) + reset() + 'world!')
print(deco('Hello, ', FG_BLUE, bold=True) + reset() + 'world!')
print(deco('Hello, ', FG_YELLOW, BG_GREEN, bold=True) + reset() + 'world!')
print(deco('Hello, ', FG_MAGENTA, bold=True) + reset() + 'w...')

warning("emmm, seems there is a small proble...")
#error('Unknown error!')


from coloredlog.color import *

const_deco = deco('', FG_MAGENTA, BG_WHITE, bold=True) 

for i in range(10): # simulates intensive use case
    print(deco('Hello world for {} times'.format(i), const_deco=const_deco))

print(reset()) # reset to normal color
