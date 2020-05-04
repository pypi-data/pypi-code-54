# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source'}

packages = \
['cuta', 'cuta.cli', 'cuta.core']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'docker>=4.2.0,<5.0.0',
 'emoji>=0.5.4,<0.6.0',
 'structlog>=20.1.0,<21.0.0',
 'typer>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['cuta = cuta.cli:base']}

setup_kwargs = {
    'name': 'cuta',
    'version': '0.1.0',
    'description': '',
    'long_description': '[![CircleCI](https://circleci.com/gh/ylathouris/bio.svg?style=shield)](https://circleci.com/gh/ylathouris/rolodex)  ![Coverage](coverage.svg)\n\n---\n\n# Cuta\n\n',
    'author': 'Yani Lathouris',
    'author_email': 'ylathouris@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ylathouris/cuta',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
