# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['hist_navigator']
install_requires = \
['prompt-toolkit', 'xonsh>=0.9.17']

setup_kwargs = {
    'name': 'xontrib-hist-navigator',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Noortheen Raja',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
