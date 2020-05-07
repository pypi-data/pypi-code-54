# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quoted']

package_data = \
{'': ['*']}

install_requires = \
['scrapy>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['quoted = quoted.quoted:main']}

setup_kwargs = {
    'name': 'quoted',
    'version': '0.1.0',
    'description': 'Feed your brain with the best quotes from multiple web portals.',
    'long_description': '# quoted\n\nFeed your brain with the best quotes from multiple web portals.\n\n## Features\n\n\n## Requirements\n\n```\ngit\npython 3x\npoetry\n```\n\n## Installation\n\n### Linux/MacOS\n\n```\n$ pip install quoted\n```\n\n### Windows\n\n\n## Usage\n\n```\n$ quoted\n\n"If you want to find the secrets of the universe, think in terms of energy, frequency and vibration."\n\t\t--Nikola Tesla\n```\n## Development\n\n### Run\n\n```\n$ poetry run quoted\n```\n\n### Build\n\n```\n$ poetry build\n```\n\nThe distribution packages are located in `dist` directory.\n\n### Publish\n\n```\n$ poetry publish\n```\n\n## Todo\n\n* Multiple WEB sources - [scrapy](https://scrapy.org/)\n* Cache\n* Colored Output - [rich](https://github.com/willmcgugan/rich)\n* Supports `bash` and `zsh`\n\n## Contribution\n\n* File bugs, feature requests in [GitHub Issues](https://github.com/rcares/quoted/issues).\n',
    'author': 'Rodrigo Cares',
    'author_email': 'rcares@gmail.com',
    'maintainer': 'Rodrigo Cares',
    'maintainer_email': 'rcares@gmail.com',
    'url': 'https://github.com/rcares/quoted/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
