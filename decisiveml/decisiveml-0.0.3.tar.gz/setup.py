# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decisiveml']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'pandas_market_calendars>=1.3.5,<2.0.0',
 'statsmodels>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'decisiveml',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'Lionel Young',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
