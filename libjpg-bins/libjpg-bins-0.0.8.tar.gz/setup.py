#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='libjpg-bins',
      description='Libraries for LibJPG Turbo on Alpine Linux',
      author='Spencer Hanson',
      url="https://github.com/spencer-hanson/libjpeg-turbo",
      version='0.0.8',
      package_data={
          'libjpg': ['*.so*']
      },
      zip_safe=False,
      packages=['libjpg'],
      long_description="""Libraries for LibJPG Turbo on Alpine Linux""",
      keywords="libjpg"
      )
