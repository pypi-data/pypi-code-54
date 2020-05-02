# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paroxython', 'paroxython.cli']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'regex>=2020.4.4,<2021.0.0',
 'sqlparse>=0.3.1,<0.4.0',
 'typed-ast>=1.4.1,<2.0.0',
 'typing-extensions>=3.7.4.2,<4.0.0.0']

entry_points = \
{'console_scripts': ['paroxython = paroxython.cli.cli:main']}

setup_kwargs = {
    'name': 'paroxython',
    'version': '0.1.17',
    'description': 'Search Python code for algorithmic features',
    'long_description': '![PyPI - Python Version](https://img.shields.io/pypi/pyversions/paroxython)\n[![Build Status](https://travis-ci.com/laowantong/paroxython.svg?branch=master)](https://travis-ci.com/laowantong/paroxython)\n[![codecov](https://img.shields.io/codecov/c/github/laowantong/paroxython/master)](https://codecov.io/gh/laowantong/paroxython)\n[![Updates](https://pyup.io/repos/github/laowantong/paroxython/shield.svg)](https://pyup.io/repos/github/laowantong/paroxython/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/laowantong/paroxython)\n\n# Paroxython\n\nComing soon.\n',
    'author': 'Aristide Grange',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laowantong/paroxython/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
