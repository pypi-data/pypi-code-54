# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fact_sphere', 'fact_sphere.facts']

package_data = \
{'': ['*'], 'fact_sphere.facts': ['audio/*']}

install_requires = \
['attrs>=18.2,<19.4']

extras_require = \
{'dev': ['coverage[toml]>=5.0,<6.0',
         'flake8>=3.5,<4.0',
         'flake8-builtins>=1.0,<2.0',
         'flake8-comprehensions>=2.0,<=4.0',
         'flake8-import-order>=0.18,<0.19',
         'flake8-import-order-tbm>=1.0,<2.0',
         'nox>=2019,<2020',
         'sphinx>=2.0,<3.0',
         'sphinx-material<1.0.0',
         'ward>=0.42.0-beta.0'],
 'doc': ['sphinx>=2.0,<3.0', 'sphinx-material<1.0.0'],
 'lint': ['flake8>=3.5,<4.0',
          'flake8-builtins>=1.0,<2.0',
          'flake8-comprehensions>=2.0,<=4.0',
          'flake8-import-order>=0.18,<0.19',
          'flake8-import-order-tbm>=1.0,<2.0'],
 'test': ['coverage[toml]>=5.0,<6.0', 'nox>=2019,<2020', 'ward>=0.42.0-beta.0']}

setup_kwargs = {
    'name': 'fact-sphere',
    'version': '1.0.1',
    'description': 'A library for Portal 2 Fact Sphere facts.',
    'long_description': "# fact-sphere\n\n[![PyPI](https://img.shields.io/pypi/v/fact-sphere.svg?label=PyPI)](https://pypi.org/project/fact-sphere/)\n![](https://img.shields.io/badge/Python-3.6%2B-blue.svg)  \n[![GitHub CI](https://img.shields.io/github/workflow/status/thebigmunch/fact-sphere/CI?label=GitHub%20CI)](https://github.com/thebigmunch/fact-sphere/actions?query=workflow%3ACI)\n[![Codecov](https://img.shields.io/codecov/c/github/thebigmunch/fact-sphere.svg?label=Codecov)](https://codecov.io/gh/thebigmunch/fact-sphere)  \n[![Docs - Stable](https://img.shields.io/readthedocs/fact-sphere/stable.svg?label=Docs%20%28Stable%29)](https://fact-sphere.readthedocs.io/en/stable/)\n[![Docs - Latest](https://img.shields.io/readthedocs/fact-sphere/latest.svg?label=Docs%20%28Latest%29)](https://fact-sphere.readthedocs.io/en/latest/)\n\n[fact-sphere](https://github.com/thebigmunch/fact-sphere) is a library for Portal 2 Fact Sphere facts\nborn from an off-handed comment during a conversation on IRC:\n``<%Ashmandias> then slap up a random fact from Portal 2's Fact Sphere``.\n\nCredit to [Portal Wiki](https://theportalwiki.com/wiki/List_of_Fact_Sphere_facts) for the reference material.\n\n\n## Installation\n\n``pip install -U fact-sphere``\n\n\n## Usage\n\nFor the release version, see the [stable docs](https://fact-sphere.readthedocs.io/en/stable/).  \nFor the development version, see the [latest docs](https://fact-sphere.readthedocs.io/en/latest/).\n\n\n## Appreciation\n\nShowing appreciation is always welcome.\n\n#### Thank\n\n[![Say Thanks](https://img.shields.io/badge/thank-thebigmunch-blue.svg?style=flat-square)](https://saythanks.io/to/thebigmunch)\n\nGet your own thanks inbox at [SayThanks.io](https://saythanks.io/).\n\n#### Contribute\n\n[Contribute](https://github.com/thebigmunch/fact-sphere/blob/master/.github/CONTRIBUTING.md) by submitting bug reports, feature requests, or code.\n\n#### Help Others/Stay Informed\n\n[Discourse forum](https://forum.thebigmunch.me/)\n\n#### Referrals/Donations\n\n[![Digital Ocean](https://img.shields.io/badge/Digital_Ocean-referral-orange.svg?style=flat-square)](https://bit.ly/DigitalOcean-tbm-referral) [![Namecheap](https://img.shields.io/badge/Namecheap-referral-orange.svg?style=flat-square)](http://bit.ly/Namecheap-tbm-referral) [![PayPal](https://img.shields.io/badge/PayPal-donate-brightgreen.svg?style=flat-square)](https://bit.ly/PayPal-thebigmunch)\n",
    'author': 'thebigmunch',
    'author_email': 'mail@thebigmunch.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thebigmunch/fact-sphere',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
