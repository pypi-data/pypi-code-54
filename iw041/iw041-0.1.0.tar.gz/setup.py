# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iw041']

package_data = \
{'': ['*']}

install_requires = \
['pandas==1.0.1']

setup_kwargs = {
    'name': 'iw041',
    'version': '0.1.0',
    'description': 'This is a test project from iw041.',
    'long_description': None,
    'author': 'Ingolf Wassmann',
    'author_email': 'ingolf.wassmann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
