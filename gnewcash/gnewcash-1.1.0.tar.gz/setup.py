# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gnewcash', 'gnewcash.file_formats']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gnewcash',
    'version': '1.1.0',
    'description': 'Python Library for reading, interacting with, and writing GnuCash files',
    'long_description': None,
    'author': 'Paul Bromwell Jr.',
    'author_email': 'pbromwelljr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
