import os
import sys
import subprocess

from setuptools import sandbox as setuptools_
from compose.cli import main as compose
from loguru import logger

from tamplar.internal import utils


class DuplicatePathException(Exception):
    """
    There are not the only path to library
    """
    pass


logger.add(sys.stdout, backtrace=False, diagnose=True)


def deps():
    logger.info('install dependencies')
    subprocess.call(['pip', 'install', '-r', 'requirements'])


def init():
    logger.info('initialize new service')
    file_path = os.path.realpath(__file__)
    print(file_path)
    root_lib_path = os.path.dirname(file_path).split('/')[:-2]
    print(file_path)
    path = '/'.join(root_lib_path)
    src = f'{path}/tamplar/template/'
    dst = os.path.abspath('./')
    utils.copytree(src=src, dst=dst)
    deps()


def run(mode='local', daemon=None):
    logger.info('run service')
    # compose.TopLevelCommand()


def upload(pypi=None, docker=None):
    args = ['bdist_wheel', 'upload']
    if pypi is not None:
        args += ['-r', pypi]
    setuptools_.run_setup('setup.py', pypi)
    if docker is None:
        return


def test(mode):
    pass
