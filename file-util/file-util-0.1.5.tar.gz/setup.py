# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_util']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'file-util',
    'version': '0.1.5',
    'description': '',
    'long_description': '# file-util\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyalev/file-util',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
