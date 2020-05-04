# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arangodb_pythongraph']

package_data = \
{'': ['*']}

install_requires = \
['pyintergraph>=1.2.0,<2.0.0', 'python-arango>=5.4.0,<6.0.0']

setup_kwargs = {
    'name': 'arangodb-pythongraph',
    'version': '0.0.1',
    'description': 'Fetch an AQL directly to a Python graph representation (In NetworkX, IGraph, or Graph-Tool)',
    'long_description': None,
    'author': 'Avi Aminov',
    'author_email': 'aviaminov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
