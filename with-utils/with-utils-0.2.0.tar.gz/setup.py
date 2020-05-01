# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['with_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'with-utils',
    'version': '0.2.0',
    'description': 'WITH utils',
    'long_description': None,
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@with-madrid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
