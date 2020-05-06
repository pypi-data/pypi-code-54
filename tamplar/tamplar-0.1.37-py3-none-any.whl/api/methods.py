import os
import sys
import subprocess

import git
from setuptools import sandbox as setuptools_
from loguru import logger

from tamplar._internal import utils


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
    print('initialize new service')
    cleaned = utils.clean_directory()
    if not cleaned:
        return
    repo_name = 'python-service-layout'
    src = f'./{repo_name}/'
    dst = os.path.abspath('./')
    git.Git(dst).clone(f'git://github.com/Hedgehogues/{repo_name}.git')
    utils.mv(src=src, dst=dst)
    deps()
    prj_name = input('Please enter project name (available letters: digits, latin alphanum, -, _, space)')
    utils.name_validator(prj_name)
    pkg_name = utils.package_name(prj_name)
    utils.mv(src=pkg_name, dst='.')


def run(mode='local', daemon=None):
    print('run service')
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
