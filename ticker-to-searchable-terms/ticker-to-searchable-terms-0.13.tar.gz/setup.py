# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ticker_to_searchable_terms']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ticker-to-searchable-terms',
    'version': '0.13',
    'description': 'Generate searchable terms for public companies based off of the ticker.',
    'long_description': 'This package is used to generate searchable terms from company ticker.\n\ncompany_obj = Company("AAPL")\ncompany_obj.terms\n\nterms is a dictionary with fields ticker, name, name_alt, kp, kp-alt',
    'author': 'Henry Becket Trotter',
    'author_email': 'beckettrotter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BecketTrotter/ticker_terms',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
