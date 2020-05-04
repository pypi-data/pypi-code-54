# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ing']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.3.0,<4.0.0',
 'requests>=2.22.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0']}

entry_points = \
{'console_scripts': ['ing = ing.console:main']}

setup_kwargs = {
    'name': 'ing',
    'version': '0.1.0',
    'description': 'It is not GANGA',
    'long_description': '[![Tests](https://github.com/ankcorp/kalam/workflows/Tests/badge.svg)](https://github.com/ankcorp/kalam/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/ankcorp/kalam/branch/master/graph/badge.svg)](https://codecov.io/gh/ankcorp/kalam)\n[![PyPI](https://img.shields.io/pypi/v/kalam.svg)](https://pypi.org/project/kalam/)\n[![Read the Docs](https://readthedocs.org/projects/kalam/badge/)](https://kalam.readthedocs.io/)\n\n# Kalam\n\nSuperpowers for writing!\n',
    'author': 'Ank',
    'author_email': 'ank@ankcorp.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ankcorp/ing',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
