# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['turbot']

package_data = \
{'': ['*'], 'turbot': ['data/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'discord-py>=1.3.3,<2.0.0',
 'dunamai>=1.1.0,<2.0.0',
 'humanize>=2.4.0,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.3,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pytz',
 'pyyaml']

entry_points = \
{'console_scripts': ['turbot = turbot:main']}

setup_kwargs = {
    'name': 'turbot',
    'version': '3.0.0',
    'description': 'Provides a Discord client and utilities for everything Animal Crossing: New Horizons.',
    'long_description': '<img align="right" src="https://raw.githubusercontent.com/theastropath/turbot/master/turbot.png" />\n\n# Turbot\n\n[![build][build-badge]][build]\n[![python][python-badge]][python]\n[![codecov][codecov-badge]][codecov]\n[![black][black-badge]][black]\n[![mit][mit-badge]][mit]\n\nA Discord bot for everything _Animal Crossing: New Horizons_.\n\n![screenshot](https://user-images.githubusercontent.com/1903876/80298832-e784fe00-8744-11ea-8c0f-dbbf81bb5fb7.png)\n\n## 🤖 Running the bot\n\nFirst install `turbot` using [`pip`](https://pip.pypa.io/en/stable/):\n\n```shell\npip install turbot\n```\n\nThen you must configure two things:\n\n1. Your Discord bot token.\n2. The list of channels you want `turbot` to monitor.\n\nTo provide your Discord bot token either set an environment variable named\n`TURBOT_TOKEN` to the token or paste it into a file named `token.txt`.\n\nFor the list of channels you can provide channel names on the command line using\nany number of `--channel "name"` options. Alternatively you can create a file\nnamed `channels.txt` where each line of the file is a channel name.\n\nMore usage help can be found by running `turbot --help`.\n\n## 📱 Using the bot\n\nOnce you\'ve connected the bot to your server, you can interact with it over\nDiscord via the following commands in any of the authorized channels.\n\n- `!help` - Provides detailed help about all of the following commands.\n\n### 🤔 User Preferences\n\nThese commands allow users to set their preferences. These preferences are used\nto make other commands more relevant, for example by converting times to the\nuser\'s preferred timezone.\n\n- `!hemisphere`\n- `!timezone`\n\n### 💸 Turnips\n\nThese commands help users buy low and sell high in the stalk market.\n\n- `!bestsell`\n- `!buy`\n- `!clear`\n- `!graph`\n- `!history`\n- `!lastweek`\n- `!oops`\n- `!predict`\n- `!reset`\n- `!sell`\n- `!turnippattern`\n\n### 🐟 Fish and Bugs\n\nProvides users with information on where and when to catch critters.\n\n- `!bugs`\n- `!fish`\n- `!new`\n\n### 🦴 Fossils & 🖼️ Art\n\nWhen a community of users tracks collectables and trades them between each\nother, everyone finishes collecting everything in the game s much more quickly\nthan they would on their own.\n\nThese commands can also help users tell fake art from real art.\n\n- `!allart`\n- `!allfossils`\n- `!art`\n- `!collect`\n- `!collected`\n- `!count`\n- `!neededfossils`\n- `!search`\n- `!uncollect`\n- `!uncollected`\n\n---\n\n[MIT][mit] © [TheAstropath][theastropath], [lexicalunit][lexicalunit] et [al][contributors]\n\n[black-badge]:      https://img.shields.io/badge/code%20style-black-000000.svg\n[black]:            https://github.com/psf/black\n[build-badge]:      https://github.com/theastropath/turbot/workflows/build/badge.svg\n[build]:            https://github.com/theastropath/turbot/actions\n[codecov-badge]:    https://codecov.io/gh/theastropath/turbot/branch/master/graph/badge.svg\n[codecov]:          https://codecov.io/gh/theastropath/turbot\n[contributors]:     https://github.com/theastropath/turbot/graphs/contributors\n[lexicalunit]:      http://github.com/lexicalunit\n[mit-badge]:        https://img.shields.io/badge/License-MIT-yellow.svg\n[mit]:              https://opensource.org/licenses/MIT\n[python-badge]:     https://img.shields.io/badge/python-3.7+-blue.svg\n[python]:           https://www.python.org/\n[theastropath]:     https://github.com/theastropath\n',
    'author': 'TheAstropath',
    'author_email': 'theastropath@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theastropath/turbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
