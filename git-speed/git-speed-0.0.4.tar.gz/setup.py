# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_speed']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['git-speed = git_speed.cli:main']}

setup_kwargs = {
    'name': 'git-speed',
    'version': '0.0.4',
    'description': 'Installs Git aliases.',
    'long_description': '# git-speed\n\nGit aliases to speed you up.\n\nSee https://www.gitscientist.com for more.\n',
    'author': 'Daniel Tipping',
    'author_email': 'daniel@oldreliable.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.gitscientist.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
