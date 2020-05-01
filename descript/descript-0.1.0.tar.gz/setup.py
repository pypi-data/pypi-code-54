# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['descript']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'descript',
    'version': '0.1.0',
    'description': 'Simple library for `descript.ion` files manipulation.',
    'long_description': 'python-descript-ion\n===================\n\n[![Build Status](https://travis-ci.org/histrio/python-descript-ion.svg?branch=master)](https://travis-ci.org/histrio/python-descript-ion)\n[![PyPI](https://img.shields.io/pypi/v/descript.svg)]()\n\nSimple library for `descript.ion` files manipulation \n\nExamples:\n---------\n\n    import descript.ion\n\n    #Read description\n    with descript.ion.open(filename) as f:\n        print f.description\n\n    #Write description\n    with descript.ion.open(filename) as f:\n        f.description = self.description\n\n    #Remove description\n    with descript.ion.open(filename) as f:\n        del f.description\n',
    'author': 'Rinat Sabitov',
    'author_email': 'rinat.sabitov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/histrio/python-descript-ion',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
