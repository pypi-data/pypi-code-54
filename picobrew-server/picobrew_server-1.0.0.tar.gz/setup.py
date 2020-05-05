# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picobrew_server',
 'picobrew_server.beerxml',
 'picobrew_server.blueprints',
 'picobrew_server.utils']

package_data = \
{'': ['*'],
 'picobrew_server': ['static/css/*',
                     'static/font/material-design-icons/*',
                     'static/font/roboto/*',
                     'static/img/*',
                     'static/js/*',
                     'templates/*']}

install_requires = \
['Flask-Cors==3.0.8',
 'Flask==1.1.2',
 'Werkzeug==1.0.1',
 'pybeerxml>=1.0.8,<2.0.0',
 'webargs==6.0.0']

setup_kwargs = {
    'name': 'picobrew-server',
    'version': '1.0.0',
    'description': 'A reverse-engineered server for the Picobrew homebrewing machines',
    'long_description': None,
    'author': 'Tom Herold',
    'author_email': 'heroldtom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hotzenklotz/picobrew-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
