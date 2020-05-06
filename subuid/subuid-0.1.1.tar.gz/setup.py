#!/usr/bin/env python

from subuid import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="subuid",
      version=__version__,
      description="Utilties to mange subuid/subgid lists",
      author="Derek Yarnell",
      author_email="derek@umiacs.umd.edu",
      url="https://gitlab.umiacs.umd.edu/derek/subuid",
      packages=["subuid", ],
      platforms="UNIX/Linux",
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Operating System :: POSIX',
                   'Intended Audience :: System Administrators',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6', ],
      scripts=["bin/addsub", ],
      )
