# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['luh3417',
 'luh3417.replace',
 'luh3417.restore',
 'luh3417.snapshot',
 'luh3417.transfer']

package_data = \
{'': ['*']}

install_requires = \
['apache-libcloud>=2.0,<3.0', 'coloredlogs>=9.0']

entry_points = \
{'console_scripts': ['luh3417_replace = luh3417.replace.__main__:__main__',
                     'luh3417_restore = luh3417.restore.__main__:__main__',
                     'luh3417_snapshot = luh3417.snapshot.__main__:__main__',
                     'luh3417_transfer = luh3417.transfer.__main__:__main__']}

setup_kwargs = {
    'name': 'luh3417',
    'version': '0.1.4',
    'description': 'A WordPress backup/restore/workflow tool',
    'long_description': None,
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
