# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdtoc']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mkdtoc = mkdtoc.mkdtoc:main']}

setup_kwargs = {
    'name': 'mkdtoc',
    'version': '0.1.0',
    'description': 'Automatically generate Table of Contents for markdown.',
    'long_description': None,
    'author': 'Hiroki Konishi',
    'author_email': 'relastle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
