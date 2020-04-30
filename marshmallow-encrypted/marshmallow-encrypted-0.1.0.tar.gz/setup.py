# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marshmallow_encrypted']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3,<4', 'pycryptodome>=3,<4']

setup_kwargs = {
    'name': 'marshmallow-encrypted',
    'version': '0.1.0',
    'description': 'Encrypted field for use with Marshmallow.',
    'long_description': None,
    'author': 'Bas Wind',
    'author_email': 'mailtobwind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
