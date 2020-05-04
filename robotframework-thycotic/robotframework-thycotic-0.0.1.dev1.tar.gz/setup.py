#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2020 Cutting Edge QA Marcin Koperski

import sys
from os.path import abspath, join, dirname
from setuptools import find_packages, setup

sys.path.append(join(dirname(__file__), "src"))

VERSION = "0.0.1.dev1"

ROOT_DIR = dirname(abspath(__file__))
SOURCE_DIR = "src"
REQUIREMENTS = ["robotframework>=3.2b1", "requests"]


setup(
    name="robotframework-thycotic",
    version=VERSION,
    description="RobotFramework Thycotic",
    license="Apache License 2.0",
    author="Marcin Koperski",
    author_email="marcin.koperski+pypi@gmail.com",
    url="https://github.com/IlfirinPL/robotframework-thycotic/",
    download_url="https://github.com/IlfirinPL/robotframework-thycotic/",
    keywords=["robotframework", "thycotic"],
    package_dir={"": SOURCE_DIR},
    package_data={"ThycoticLibrary": ["VERSION"]},
    install_requires=REQUIREMENTS,
    packages=find_packages(SOURCE_DIR),
)
