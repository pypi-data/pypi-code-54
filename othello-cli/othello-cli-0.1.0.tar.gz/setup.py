# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['othello', 'othello.agent', 'othello.game']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'agents': ['human = othello.agent.human:Human',
            'random = othello.agent.random_bot:RandomBot'],
 'console_scripts': ['othello = othello.__main__:main']}

setup_kwargs = {
    'name': 'othello-cli',
    'version': '0.1.0',
    'description': 'CLI Othello with bots',
    'long_description': '[![Tests](https://github.com/ahlaw/othello/workflows/Tests/badge.svg)](https://github.com/cjolowicz/hypermodern-python/actions?workflow=Tests)\n\n\n# othello\n\nA command-line interface for Othello! Either player can be human or a bot.\nA list of available agents is available via the help command.\n\n\n## Installation\n\nTo install the Othello project, run this command in your terminal:\n\n```\n$ pip install othello\n```\n\n\n## Usage\n\n```\n$ othello [OPTIONS]\n\n    -b <agent>, --black <agent>\n    -w <agent>, --white <agent>\n    -v, --version\n    -h, --help\n```\n\n\n## License\n\n[MIT License](LICENSE.md)\n',
    'author': 'Amos Law',
    'author_email': 'amos.law98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ahlaw/othello',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
