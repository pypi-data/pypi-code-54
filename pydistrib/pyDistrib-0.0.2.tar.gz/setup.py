# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydistrib', 'pydistrib.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydistrib',
    'version': '0.0.2',
    'description': 'A package to distribute Python computations across devices',
    'long_description': None,
    'author': 'Rayan Hatout',
    'author_email': 'rayan.hatout@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rayanht/pyDistrib',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
