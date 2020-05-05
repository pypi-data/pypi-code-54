#!/usr/bin/env python

import os
from setuptools import setup

setup(
    name = "ioc-parser-ng",
    version = "0.9.2",
    author = "Kimmo Linnavuo",
    author_email = "kimmo.linnavuo@gmail.com",
    scripts = ['bin/iocp-ng'],
    description = ("Tool to extract indicators of compromise from security reports, next generation"),
    license = "MIT",
    url = "https://gitlab.com/cincan/ioc_parser",
    packages = ['iocp'],
    include_package_data = True,
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires = open("requirements.txt").read().splitlines(),
    python_requires='>=3.5',
)
