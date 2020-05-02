# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['k3s_status_lcd']

package_data = \
{'': ['*']}

install_requires = \
['i2c_lcd>=0.1.0,<0.2.0', 'kubernetes>=11.0.0,<12.0.0']

setup_kwargs = {
    'name': 'k3s-status-lcd',
    'version': '0.1.1',
    'description': 'A small service to retrive the status of a k3s cluster on a Raspberry Pi and render on an attached LCD',
    'long_description': None,
    'author': 'Mark Woolley',
    'author_email': 'mw@marknet15.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
