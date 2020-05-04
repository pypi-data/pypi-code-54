# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrobud',
 'pyrobud.core',
 'pyrobud.custom_modules',
 'pyrobud.modules',
 'pyrobud.util']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'aiorun>=2019.11.1,<2021.0.0',
 'beauty-print>=0.6.0,<0.7.0',
 'colorlog>=4.1.0,<5.0.0',
 'emoji>=0.5.4,<0.6.0',
 'gitpython>=3.0.5,<4.0.0',
 'meval>=2.5,<3.0',
 'msgpack>=0.6.2,<1.1.0',
 'pillow>=6.2.2,<8.0.0',
 'plyvel>=1.1.0,<2.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'sentry-sdk>=0.13.5,<0.15.0',
 'speedtest-cli>=2.1.2,<3.0.0',
 'telethon>=1.10.10,<2.0.0',
 'tomlkit>=0.5.8,<0.7.0']

extras_require = \
{'fast': ['cryptg>=0.2.post0,<0.3']}

entry_points = \
{'console_scripts': ['pyrobud = pyrobud.main:main']}

setup_kwargs = {
    'name': 'pyrobud',
    'version': '2.1.0',
    'description': 'A clean selfbot for Telegram with an emphasis on quality and practicality.',
    'long_description': '<p align="center">\n    <img width="200" height="200" src="https://raw.githubusercontent.com/kdrag0n/pyrobud/master/assets/logo.png">\n</p>\n\n<h1 align="center">Pyrobud</h1>\n\n<p align="center">\n    <a href="https://github.com/kdrag0n/pyrobud/releases"><img src="https://img.shields.io/github/v/tag/kdrag0n/pyrobud?sort=semver" alt="Latest tag"></a>\n    <a href="https://github.com/kdrag0n/pyrobud/actions?query=workflow%3A%22Build+%26+publish+Docker+image%22"><img src="https://img.shields.io/github/workflow/status/kdrag0n/pyrobud/Build%20%26%20publish%20Docker%20image" alt="CI status"></a>\n    <a href="https://t.me/pyrobud"><img src="https://img.shields.io/badge/chat-on%20telegram-blueviolet" alt="Telegram chat"></a>\n</p>\n\nPyrobud is a clean selfbot for Telegram with an emphasis on quality and\npracticality.\n\nIt\'s designed to complement the official clients rather than replace them as\nmany other selfbots tend to lean towards. It is written in Python using\nthe [Telethon](https://github.com/LonamiWebs/Telethon) library.\n\nA working installation of **Python 3.6** or newer is required to run Pyrobud.\n\n## Compatibility\n\nPyrobud should be compatible with all major operating systems. While it has not\nbeen officially tested on Windows or macOS, there should not be anything\npreventing it from working on those platforms. Please let me know if you\'ve\ngotten it working so I can add it here.\n\nIt is also possible to run the bot on a smartphone. On Android it can be done\nwith the [Termux](https://wiki.termux.com/wiki/Main_Page) app, and on iOS it\nshould be possible using the [iSH](https://ish.app/) app.\n\n## Installation\n\n### Native dependencies\n\nPyrobud uses the native LevelDB library for its database, so you\'ll need to\ninstall that first. Below are instructions for some common operating systems:\n\n| OS/Distro    | Command                      |\n| ------------ | ---------------------------- |\n| Arch Linux   | `pacman -S leveldb`          |\n| Ubuntu       | `apt install libleveldb-dev` |\n| macOS        | `brew install leveldb`       |\n| Termux       | `apt install leveldb`        |\n| FreeBSD      | `pkg install leveldb`        |\n\n### Using Docker\n\nSimply run `docker run --rm -itv "$PWD/data:/data" kdrag0n/pyrobud` to run the\nlatest unstable version with the data directory set to `data` in the current\nworking directory. Feel free to customize the data directory as you wish, as\nlong as you create `config.toml` in your chosen data directory using the\ninstructions below. The data section of the Docker command should always look\nlike `-v "/path/to/data:/data"`.\n\nNote that the official Docker image only supports Linux x86_64. Other operating\nsystems and architectures are not supported. However, pull requests contributing\nsuch support are welcome.\n\n### Using pip\n\nWhen using pip, it\'s highly recommended to install everything inside a virtual\nenvironment to minimize contamination of the system Python install, since many\nof the bot\'s dependencies are not typically packaged by Linux distributions.\nSuch environments can easily be created using the following command:\n`python3 -m venv [target directory]`\n\nThey can then be activated using `source [target directory]/bin/activate` or the\nequivalent command and script for your shell of choice.\n\nYou can still install all the dependencies in your system Python environment,\nbut please be aware of the potential issues when doing so. The installed packages\nmay conflict with the system package manager\'s installed packages, which can\ncause trouble down the road and errors when upgrading conflicting packages.\n**You have been warned.**\n\n### Stable\n\nYou can obtain the latest stable version from PyPI:\n\n`python3 -m pip install pyrobud`\n\nIf you have or can install OpenSSL development headers, installing the `fast`\nvariant is highly recommended:\n\n`python3 -m pip install pyrobud[fast]`\n\nWithout the `cryptg` encryption acceleration library from the `fast` extras, the\nbot will be **extremely slow** when dealing with any files, even small ones.\nDownload and upload speeds can be as slow as kilobytes per second without this\nlibrary.\n\n### Bleeding-edge\n\nFirst, clone this Git repository locally:\n`git clone https://github.com/kdrag0n/pyrobud`\n\nAfter that, you can run `python3 -m pip install .` to install the bot along with\nthe bare minimum dependencies. However, including the `fast` extras is highly\nrecommended to improve performance: `python3 -m pip install .[fast]`\n\nRead the section above for more information on what `fast` does and why you\nshould use it.\n\nOnce it\'s installed, you can choose to invoke it using the `pyrobud` command, or\nrun the bot in-place (which is described later in the Usage section). Running it\nin-place is recommended to allow for automatic updates via Git.\n\n#### Error: `Directory \'.\' is not installable. File \'setup.py\' not found.`\n\nThis common error is caused by an outdated version of pip. We use the Poetry\npackage manager to make things easier to maintain, which works with pip through\nPEP-517. This is a relatively new standard, so a newer version of pip is necessary\nto make it work.\n\nUpgrade to pip 19 to fix this issue: `pip3 install -U pip`\n\n## Configuration\n\nCopy `config.example.toml` to `config.toml` and edit the settings as desired.\nEach and every setting is documented by the comments above it.\n\nObtain the API ID and hash from [Telegram\'s website](https://my.telegram.org/apps).\n**TREAT THESE SECRETS LIKE A PASSWORD!**\n\nConfiguration must be complete before starting the bot for the first time for it\nto work properly.\n\n## Usage\n\nTo start the bot, type `python3 main.py` if you are running it in-place or use\ncommand corresponding to your chosen installation method above.\n\nWhen asked for your phone number, it is important that you type out the **full**\nphone number of your account, including the country code, without any symbols\nsuch as spaces, hyphens, pluses, or parentheses. For example, the US number\n`+1 (234) 567-8910` would be entered as `12345678910`. Any other format will be\nrejected by Telegram.\n\nAfter the bot has started, you can run the `help` command to view all the\navailable commands and modules. This can be done anywhere on Telegram as long as\nyou prepend the command prefix to the name of the command you wish to invoke.\nThe default prefix (if you haven\'t changed it in the config) is `.`, so one\nwould type `.help` to run the command. All other commands work the same way,\nsave for snippet replacements which are used with `/snipname/` anywhere in a\nmessage.\n\n## Deployment\n\nFor long-term server deployments, an example systemd service is available\n[here](https://github.com/kdrag0n/pyrobud/blob/master/systemd/pyrobud.service).\nIt is strongly recommended to use this service for any long-term deployments as\nit it includes parameters to improve security and restrict the system resources\nthe bot can utilize to limit damage if something goes awry. The example assumes\nthat the bot will run under an independent user named `pyrobud` with a virtual\nenvironment located at `/home/pyrobud/venv` and a Git clone of the bot located\nat `/home/pyrobud/pyrobud`. This setup avoids tainting the system\'s Python install\nwith unmanaged packages and allows the bot to self-update using Git.\n\nIf you\'re using Docker to run the bot, use [pyrobud-docker.service](https://github.com/kdrag0n/pyrobud/blob/master/systemd/pyrobud-docker.service)\ninstead.\n\n`tmux` or `screen` should never be used to run the bot in production. A supervisor,\nunlike a terminal multiplexer, contains a plethora of features crucial for proper\ndeployments: automatic ratelimited restarting, logging, monitoring, and more. Some,\nsuch as systemd, also support limiting resources and and imposing restrictions for\nsecurity. A shell script that invokes Python in a `while` loop is not a replacement\nfor a proper supervisor.\n\n## Contributing\n\nSee the [Contribution Guidelines](https://github.com/kdrag0n/pyrobud/blob/master/CONTRIBUTING.md)\nfor more information.\n\n## Module Development\n\nYou can easily develop custom modules! See the\n[Module Development Handbook](https://github.com/kdrag0n/pyrobud/blob/master/DEVELOPMENT.md)\nfor more information.\n\n## Support\n\nFeel free to join the [official support group](https://t.me/pyrobud) on Telegram\nfor help or general discussion regarding the bot. You may also\n[open an issue on GitHub](https://github.com/pyrobud/pyrobud/issues) for bugs,\nsuggestions, or anything else relevant to the project.\n',
    'author': 'Danny Lin',
    'author_email': 'danny@kdrag0n.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kdrag0n/pyrobud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
