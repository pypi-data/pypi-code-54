# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['assert_info']

package_data = \
{'': ['*']}

install_requires = \
['asttokens>=2.0.4,<3.0.0', 'docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['assert-info = assert_info:main']}

setup_kwargs = {
    'name': 'assert-info',
    'version': '0.1.1',
    'description': 'A tool for fixing bare assert statements',
    'long_description': None,
    'author': 'Samuel Broster',
    'author_email': 's.h.broster+gitlab@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/broster/assert-info',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
