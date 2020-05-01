#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='libpng-bins',
      description='Libraries for LibPNG on Alpine Linux',
      author='Spencer Hanson',
      url="https://github.com/spencer-hanson/libpng",
      version='0.0.3',
      package_data={
          'libpng': ['*.so*', '*.la*']
      },
      zip_safe=False,
      packages=['libpng'],
      long_description="""Libraries for LibPNG on Alpine Linux""",
      keywords="libpng"
      )
