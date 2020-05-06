# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['readsql']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['readsql = readsql.__main__:command_line']}

setup_kwargs = {
    'name': 'readsql',
    'version': '0.1.0',
    'description': 'Convert SQL to most human readable format',
    'long_description': '# readsql\n\nConvert SQL to most human readable format\n\n# Usage\n\n- `python readsql tests/sql_example.sql` converts example SQL code to easier readable format\n- `python readsql "select gold from mine" -s` takes the `"select gold from mine"` string as input and outputs it formatted\n\n# Testing\n\nHave `pytest` installed and run `pytest -v` (-v stands for verbose)\n',
    'author': 'Azis',
    'author_email': 'azuolas.krusna@yahoo.com',
    'maintainer': 'Azis',
    'maintainer_email': 'azuolas.krusna@yahoo.com',
    'url': 'https://github.com/AzisK/readsql/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
