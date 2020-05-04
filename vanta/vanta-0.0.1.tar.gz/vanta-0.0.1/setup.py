# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vanta']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'flake8-bugbear>=20.1.4,<21.0.0',
 'flake8-builtins>=1.5.2,<2.0.0',
 'flake8-coding>=1.3.2,<2.0.0',
 'flake8-commas>=2.0.0,<3.0.0',
 'flake8-comprehensions>=3.2.2,<4.0.0',
 'flake8-debugger>=3.2.1,<4.0.0',
 'flake8-deprecated>=1.3,<2.0',
 'flake8-fixme>=1.1.1,<2.0.0',
 'flake8-isort>=3.0.0,<4.0.0',
 'flake8-mutable>=1.2.0,<2.0.0',
 'flake8-pep3101>=1.3.0,<2.0.0',
 'flake8-tidy-imports>=4.1.0,<5.0.0',
 'flake8-tuple>=0.4.1,<0.5.0',
 'isort>=4.3.21,<5.0.0']

setup_kwargs = {
    'name': 'vanta',
    'version': '0.0.1',
    'description': 'Blacker than black',
    'long_description': None,
    'author': 'Dan Palmer',
    'author_email': 'dan@danpalmer.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
