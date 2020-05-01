# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konverter', 'konverter.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.3,<2.0.0', 'typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['konverter = konverter.__main__:run']}

setup_kwargs = {
    'name': 'keras-konverter',
    'version': '0.1.0',
    'description': 'A tool to convert simple Keras models to pure Python + NumPy',
    'long_description': None,
    'author': 'Shane Smiskol',
    'author_email': 'shane@smiskol.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
