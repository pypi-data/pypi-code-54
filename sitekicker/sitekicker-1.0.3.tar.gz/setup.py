# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sitekicker', 'sitekicker.entry', 'sitekicker.folder']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4',
 'jinja2',
 'markdown',
 'pygments',
 'pymdown-extensions',
 'pyyaml',
 'watchdog']

setup_kwargs = {
    'name': 'sitekicker',
    'version': '1.0.3',
    'description': 'Another static site generator',
    'long_description': None,
    'author': 'Minghao Ni',
    'author_email': 'niminghao804@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nmhnmh/sitekicker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
