# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_admin_favorite_filters', 'django_admin_favorite_filters.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.1']

setup_kwargs = {
    'name': 'django-admin-favorite-filters',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yigit Guler',
    'author_email': 'yigit@hipo.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
