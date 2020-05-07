# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['domainprops']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'domainprops',
    'version': '0.1.0',
    'description': 'Parse domain name properties.',
    'long_description': None,
    'author': 'Viktor Persson',
    'author_email': 'viktor.persson@arcsin.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
