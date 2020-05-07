# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['storage_bucket']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'google-cloud-storage>=1.28.1,<2.0.0',
 'returns>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'storage-bucket',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thomas Borgen',
    'author_email': 'thomas@borgenit.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
