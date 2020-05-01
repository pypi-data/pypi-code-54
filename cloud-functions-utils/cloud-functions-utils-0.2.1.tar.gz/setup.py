# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloud_functions_utils']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=1.24.0,<2.0.0',
 'google-cloud-error-reporting>=0.33.0,<0.34.0',
 'google-cloud-pubsub>=1.4.3,<2.0.0',
 'google-cloud-storage>=1.28.0,<2.0.0']

setup_kwargs = {
    'name': 'cloud-functions-utils',
    'version': '0.2.1',
    'description': 'Utilities for Google Cloud Functions.',
    'long_description': None,
    'author': 'Jan-Benedikt Jagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
