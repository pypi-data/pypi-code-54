# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topological_sort_backport']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'topological-sort-backport',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jonas Bulik',
    'author_email': 'jonas@bulik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
