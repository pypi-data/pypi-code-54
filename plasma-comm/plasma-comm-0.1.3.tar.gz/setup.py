# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plasma_comm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'plasma-comm',
    'version': '0.1.3',
    'description': 'Common code for plasma opensource packages.',
    'long_description': None,
    'author': 'Damian Krystkiewicz',
    'author_email': 'damian.krystkiewicz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
