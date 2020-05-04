# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'textract-trp',
    'version': '0.1.0',
    'description': 'Parser for Amazon Textract results.',
    'long_description': '',
    'author': 'Michael Ludvig',
    'author_email': 'mludvig@logix.net.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mludvig/amazon-textract-trp',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
