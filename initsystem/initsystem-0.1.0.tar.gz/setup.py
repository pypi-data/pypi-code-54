# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['initsystem']
setup_kwargs = {
    'name': 'initsystem',
    'version': '0.1.0',
    'description': 'init-system-agnostic way to start, stop and check statuses of services',
    'long_description': None,
    'author': 'ewen-lbh',
    'author_email': 'ewen.lebihan7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
