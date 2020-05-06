# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_updater']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'ehelply-logger>=0.0.8,<0.0.9',
 'pydantic>=1.5.1,<2.0.0',
 'python-slugify>=4.0.0,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'wheel>=0.34.2,<0.35.0']

setup_kwargs = {
    'name': 'ehelply-updater',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Updater\nMicroservice updater\n',
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
