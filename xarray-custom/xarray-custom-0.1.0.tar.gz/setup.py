# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_custom']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18,<2.0', 'xarray>=0.15,<0.16']

setup_kwargs = {
    'name': 'xarray-custom',
    'version': '0.1.0',
    'description': 'Data classes for custom xarray constructors',
    'long_description': '# xarray-custom\n:zap: Data classes for custom xarray constructors\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/xarray-custom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
