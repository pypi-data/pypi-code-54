# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nicevk', 'nicevk.plugins']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.13.0,<0.14.0', 'vkbottle>=2.7.2,<3.0.0']

entry_points = \
{'console_scripts': ['nicevk = nicevk:cli.run']}

setup_kwargs = {
    'name': 'nicevk',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'nm17',
    'author_email': 'dannevergame@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
