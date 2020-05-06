import os
import sys
import subprocess

import git
from setuptools import sandbox as setuptools_
from loguru import logger
from string import digits, ascii_lowercase

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


def name_validator(project_name):
    name_symbols = set(project_name.lower())
    all_symbols = ascii_lowercase + digits + ' -_'
    intersection = name_symbols.intersection(all_symbols)
    assert len(intersection) < len(name_symbols), 'invalid project name'


def package_name(name):
    return name.replace('-', '_').replace(' ', '_')


def clean_directory():
    files = os.listdir(path='.')
    if len(files) == 0:
        return
    clean = input("Directory is not empty. All files will be remove [Y/n]:")
    clean = clean.lower()
    assert clean in ['y', 'n', '']
    if clean == 'n':
        return False
    return True


def init():
    logger.info('initialize new service')
    cleaned = clean_directory()
    if not cleaned:
        return
    repo_name = 'python-service-layout'
    src = f'./{repo_name}/'
    dst = os.path.abspath('./')
    git.Git(dst).clone(f'git://github.com/Hedgehogues/{repo_name}.git')
    utils.mv(src=src, dst=dst)
    deps()
    prj_name = input('Please enter project name (available letters: digits, latin alphanum, -, _, space)')
    name_validator(prj_name)
    pkg_name = package_name(prj_name)
    utils.mv(src=pkg_name, dst='.')


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
