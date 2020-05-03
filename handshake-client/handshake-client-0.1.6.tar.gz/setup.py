# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['handshake_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'python-bitcoinrpc>=1.0,<2.0',
 'python-socketio[client]>=4.5.1,<5.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'handshake-client',
    'version': '0.1.6',
    'description': 'Handshake API client by Python',
    'long_description': None,
    'author': 'naoki-maeda',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
