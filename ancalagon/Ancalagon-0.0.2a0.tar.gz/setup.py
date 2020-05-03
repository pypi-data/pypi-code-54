# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ancalagon', 'ancalagon.responses']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ancalagon',
    'version': '0.0.2a0',
    'description': 'The blackest ASGI framework',
    'long_description': None,
    'author': 'Nimond',
    'author_email': 'dndnomin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
