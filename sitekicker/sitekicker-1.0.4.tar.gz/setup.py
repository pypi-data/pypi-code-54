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

entry_points = \
{'console_scripts': ['sitekicker = sitekicker.__main__:main',
                     'sk = sitekicker.__main__:main']}

setup_kwargs = {
    'name': 'sitekicker',
    'version': '1.0.4',
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
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
