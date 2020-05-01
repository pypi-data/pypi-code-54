# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sanic_function_deps']

package_data = \
{'': ['*']}

install_requires = \
['sanic>=19.12.2,<20.0.0']

setup_kwargs = {
    'name': 'sanic-function-deps',
    'version': '0.2.0',
    'description': 'Directly inject your query params & headers into your router function',
    'long_description': None,
    'author': 'Erik Lilja',
    'author_email': 'erikvlilja@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
