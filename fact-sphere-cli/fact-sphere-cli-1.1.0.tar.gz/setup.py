# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fact_sphere_cli']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2,<2.0', 'click>=6.0', 'fact-sphere>=1.0.1,<2.0.0']

extras_require = \
{'dev': ['flake8>=3.5,<4.0',
         'flake8-builtins>=1.0,<2.0',
         'flake8-comprehensions>=2.0,<=4.0',
         'flake8-import-order>=0.18,<0.19',
         'flake8-import-order-tbm>=1.0,<2.0',
         'nox>=2019,<2020'],
 'lint': ['flake8>=3.5,<4.0',
          'flake8-builtins>=1.0,<2.0',
          'flake8-comprehensions>=2.0,<=4.0',
          'flake8-import-order>=0.18,<0.19',
          'flake8-import-order-tbm>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['fact-sphere = fact_sphere_cli.cli:fact_sphere_cli']}

setup_kwargs = {
    'name': 'fact-sphere-cli',
    'version': '1.1.0',
    'description': 'A CLI for Portal 2 Fact Sphere facts.',
    'long_description': '# fact-sphere-cli\n\n[![PyPI](https://img.shields.io/pypi/v/fact-sphere-cli.svg?label=PyPI)](https://pypi.org/project/fact-sphere-cli/)\n![](https://img.shields.io/badge/Python-3.6%2B-blue.svg)  \n[![GitHub CI](https://img.shields.io/github/workflow/status/thebigmunch/fact-sphere-cli/CI?label=GitHub%20CI)](https://github.com/thebigmunch/fact-sphere-cli/actions?query=workflow%3ACI)  \n\n[fact-sphere-cli](https://github.com/thebigmunch/fact-sphere-cli) is a CLI for Portal 2 Fact Sphere facts using the\n[fact-sphere](https://github.com/thebigmunch/fact-sphere) library.\n\n\n## Installation\n\n``pip install -U fact-sphere-cli``\n\n\n## Usage\n\n```\nUsage: fact-sphere [OPTIONS] COMMAND\n\n  A CLI for Portal 2 Fact Sphere facts.\n\nOptions:\n  -V, --version  Show the version and exit.\n  -h, --help     Show this message and exit.\n\nCommands:\n  text*  Get the text for a random fact.\n  audio  Get the filepath or file content for a random fact.\n  fact   Get the text, filepath, and type for a random fact.\n```\n\nA plain ``fact-sphere`` call defaults to running the ``text`` command.\n\nThe only option is for the ``audio`` command. Use ``--read`` option\nto output the binary file content of the audio for piping.\n\n\n## Appreciation\n\nShowing appreciation is always welcome.\n\n#### Thank\n\n[![Say Thanks](https://img.shields.io/badge/thank-thebigmunch-blue.svg?style=flat-square)](https://saythanks.io/to/thebigmunch)\n\nGet your own thanks inbox at [SayThanks.io](https://saythanks.io/).\n\n#### Contribute\n\n[Contribute](https://github.com/thebigmunch/fact-sphere-cli/blob/master/.github/CONTRIBUTING.md) by submitting bug reports, feature requests, or code.\n\n#### Help Others/Stay Informed\n\n[Discourse forum](https://forum.thebigmunch.me/)\n\n#### Referrals/Donations\n\n[![Digital Ocean](https://img.shields.io/badge/Digital_Ocean-referral-orange.svg?style=flat-square)](https://bit.ly/DigitalOcean-tbm-referral) [![Namecheap](https://img.shields.io/badge/Namecheap-referral-orange.svg?style=flat-square)](http://bit.ly/Namecheap-tbm-referral) [![PayPal](https://img.shields.io/badge/PayPal-donate-brightgreen.svg?style=flat-square)](https://bit.ly/PayPal-thebigmunch)\n',
    'author': 'thebigmunch',
    'author_email': 'mail@thebigmunch.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thebigmunch/fact-sphere-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
