
import sys
sys.path.append('..')

import logging, coloredlog
logging.basicConfig(
    format='%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
    handlers=[coloredlog.ConsoleHandler()],
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

logger.info('logging started')
logger.debug('debug message')
logger.info('informative')
logger.log(coloredlog.NOTIFY, 'notification')
logger.warning('a warning message')
logger.error('message on error occurred')
try:
    raise RuntimeError('An exception!')
except:
    logger.exception('Exception:')
logger.critical('THIS IS CRITICAL')


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
