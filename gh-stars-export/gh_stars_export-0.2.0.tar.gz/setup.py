# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gh_stars_export']
install_requires = \
['PyGithub>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['gh_stars_export = gh_stars_export:main']}

setup_kwargs = {
    'name': 'gh-stars-export',
    'version': '0.2.0',
    'description': 'This script exports your github stars to a json file.',
    'long_description': None,
    'author': 'Ayush Shanker',
    'author_email': 'ayushshanker@outlook.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
