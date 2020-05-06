# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_cli', 'aiogram_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=3.0.0-alpha.4,<4.0.0', 'cleo>=0.8.1,<0.9.0']

entry_points = \
{'aiogram_cli.plugins': ['builtin-about = '
                         'aiogram_cli.commands.about:AboutCommand',
                         'builtin-plugins = '
                         'aiogram_cli.commands.plugins:PluginsListCommand'],
 'console_scripts': ['aiogram = aiogram_cli.main:main',
                     'aiogram-cli = aiogram_cli.main:main']}

setup_kwargs = {
    'name': 'aiogram-cli',
    'version': '0.0.1a3',
    'description': 'aiogram CLI',
    'long_description': '# aiogram-cli\n\nCommand line interface for developers\n\nWorks only with [aiogram](https://github.com/aiogram/aiogram) 3.0+ (Is under development)\n\nHere is only bootstrap for CLI interface with extensions based on [pkg_resources](https://setuptools.readthedocs.io/en/latest/pkg_resources.html)\n\n## Installation\n\n### From PyPi\n`pip install --extra-index-url https://dev-docs.aiogram.dev/simple --pre aiogram-cli`\n\n### Poetry\n\nAdd this block to `pyproject.toml` file:\n```toml\n[[tool.poetry.source]]\nname = "aiogram-dev"\nurl = "https://dev-docs.aiogram.dev/simple"\nsecondary = true\n```\n\nAnd then run: `poetry add -D aiogram-cli`\n\n## Extensions\n\n- `aiogram_cli_generator` (WIP) - Project files generator based on pre-defined cookiecutter templates\n- `aiogram_cli_executor` (WIP) - Executor for bots\n- ...\n\n## Usage\n\nJust run in terminal `aiogram-cli` (Or alias - `aiogram`) and see what you can do with it.\n\n## Example\n\n![main interface](assets/cli.png)\n\n![commands](assets/commands.png)\n\n\n## Writing extensions\n\nAny **aiogram-cli** extension package should provide an entry point like this:\n```\n[aiogram_cli.plugins]\nmy_extension = my_package.module:MyCommand\n```\n\nOr with poetry like this:\n```toml\n[tool.poetry.plugins."aiogram_cli.plugins"]\n"builtin-about" = "aiogram_cli.commands.about:AboutCommand"\n"builtin-plugins" = "aiogram_cli.commands.plugins:PluginsListCommand"\n```\n\nThis application is based on [cleo](https://cleo.readthedocs.io/en/latest/) framework and that mean all plugins should be one of:\n1. subclass of `cleo.Command`\n1. instance of `cleo.Command`\n1. sequence of subclasses or instances of `cleo.Command`\n1. callable which accepts `app: cleo.Application` and returns any of 1-3 formats\n\nExamples:\n[aiogram_cli.commands.about](aiogram_cli/commands/about.py)\n[aiogram_cli.commands.plugins](aiogram_cli/commands/plugins.py)\n',
    'author': 'Alex Root Junior',
    'author_email': 'jroot.junior@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://aiogram.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
