# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['damn', 'damn.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0,<4.0']

setup_kwargs = {
    'name': 'django-damn',
    'version': '0.3.0',
    'description': 'Django asset dependency management.',
    'long_description': None,
    'author': 'Curtis Maloney',
    'author_email': 'curtis@tinbrain.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/funkybob/django-amn',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
