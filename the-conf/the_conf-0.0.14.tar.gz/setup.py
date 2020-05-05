#!/usr/bin/env python3
import unittest
from setuptools import setup


def the_conf_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='the_conf',
      version='0.0.14',
      description='Config build from multiple sources',
      keywords='conf configuration json yaml command line environ',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
      license="GPLv3",
      author="François Schmidts",
      author_email="francois@schmidts.fr",
      maintainer="François Schmidts",
      maintainer_email="francois@schmidts.fr",
      packages=['the_conf'],
      url='https://github.com/jaesivsm/the_conf/',
      install_requires=['PyYAML==5.3'],
      test_suite='setup.the_conf_test_suite',
      )
