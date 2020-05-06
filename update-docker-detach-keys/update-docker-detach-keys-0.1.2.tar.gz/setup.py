# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['update_docker_detach_keys']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'json-file>=0.1.6,<0.2.0']

entry_points = \
{'console_scripts': ['update-docker-detach-keys = '
                     'update_docker_detach_keys.cli:cli']}

setup_kwargs = {
    'name': 'update-docker-detach-keys',
    'version': '0.1.2',
    'description': '',
    'long_description': '# update-docker-detach-keys\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
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
