# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ovretl', 'ovretl.prices_utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'ovretl',
    'version': '0.1.0',
    'description': 'Python package for Ovrsea ETL',
    'long_description': '',
    'author': 'nicolas67',
    'author_email': 'nicolas@ovrsea.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
