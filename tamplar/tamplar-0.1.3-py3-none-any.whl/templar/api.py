import os
import sys
import shutil

from loguru import logger
import subprocess


class DuplicatePathException(Exception):
    """
    There are not the only path to library
    """
    pass


logger.add(sys.stdout, backtrace=False, diagnose=True)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def deps():
    subprocess.call(['pip', 'install', '-r', 'requirements'])


def init():
    paths = list(set([p for p in sys.path if p.split('/')[-1] == 'tamplar']))
    if len(paths) != 1:
        raise DuplicatePathException()
    src = paths[0]+'/template/'
    dst = os.path.abspath('./')
    copytree(src=src, dst=dst)
