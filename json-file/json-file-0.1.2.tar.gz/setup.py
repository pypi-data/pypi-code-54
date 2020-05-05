# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['json_file']

package_data = \
{'': ['*']}

install_requires = \
['file-util>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'json-file',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
