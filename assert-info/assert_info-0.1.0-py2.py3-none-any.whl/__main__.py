"""Assert Info.

Usage:
  assert_info.py FILE... [--verbose]

Options:
  -h --help     Show this screen.
  --verbose     Verbose output
"""
from docopt import docopt
from shutil import copy
import logging
import os

from .assert_token import fixed_text

logger = logging.getLogger()
sh = logging.StreamHandler()
logger.addHandler(sh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Assert Info 1.0')

    if arguments["--verbose"]:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    for filename in arguments["FILE"]:
        text = fixed_text(filename)

        tmp_filename = filename + ".tmp"
        try:
            with open(tmp_filename, "w") as temp:
                temp.write(text)
            copy(temp.name, filename)
        finally:
            os.remove(tmp_filename)