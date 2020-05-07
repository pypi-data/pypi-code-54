import setuptools
import os

from setuptools import setup

setup(
    name="oo-tools",
    version='0.1.0',
    url="",
    author="Wesley Uykimpang",
    description="Some object-oriented classes + utilities for python",
    packages=setuptools.find_packages(),
    install_requires=['pyyaml', 'requests'],
    python_requires = ">=3.6",
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    package_data={'oo_tools': ['*.py']}
)
