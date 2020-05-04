#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c)
:license: MIT, see LICENSE for more details.
"""
import os
import sys

from setuptools import setup
from setuptools.command.install import install

# current version
VERSION = "0.0.4"


def readme():
    """print long description"""
    with open('README.rst') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="helloworld-eduardo",
    version=VERSION,
    description="Hello World or name",
    long_description=readme(),
    url="https://bitbucket.org/eduardodeasousa/hello",
    author="Eduardo Sousa",
    author_email="eduardodeasousa@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords='helloworld',
    package_dir={"": "src"},
    # packages=['hello'],
    py_modules=["helloworld"],
    install_requires=[],
    python_requires='>=3',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
