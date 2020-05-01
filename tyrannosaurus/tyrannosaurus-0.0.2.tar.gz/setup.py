# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyrannosaurus']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1,<8.0',
 'importlib-metadata>=1.6,<2.0',
 'sphinx-autoapi>=1.3,<2.0',
 'sphinx-rtd-theme>=0.4.3,<0.5.0',
 'toml>=0.10,<0.11']

entry_points = \
{'console_scripts': ['tyrannosaurus = tyrannosaurus.cli:cli']}

setup_kwargs = {
    'name': 'tyrannosaurus',
    'version': '0.0.2',
    'description': 'Generate ready-to-go Python projects.',
    'long_description': "# Tyrannosaurus Reqs\n\n[![Build status](https://img.shields.io/pypi/status/tyrannosaurus)](https://pypi.org/project/tyrannosaurus/)\n[![Latest version on PyPi](https://badge.fury.io/py/tyrannosaurus.svg)](https://pypi.org/project/tyrannosaurus/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/tyrannosaurus.svg)](https://pypi.org/project/tyrannosaurus/)\n[![Documentation status](https://readthedocs.org/projects/tyrannosaurus/badge/?version=latest&style=flat-square)](https://readthedocs.org/projects/tyrannosaurus/)\n[![Travis](https://travis-ci.org/dmyersturnbull/tyrannosaurus.svg?branch=master)](https://travis-ci.org/dmyersturnbull/tyrannosaurus)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\nAn opinionated 2020 Python template.\nJust clone it and modify or run `tyrannosaurus new`.\n\n⚠ Status: Under development\n\nProvides `tyrannosaurus sync` to copy metadata from your `pyproject.toml` other config files,\nincluding `tox.ini`, `.flake8`, `docs/conf.py`, `docs/requirements.txt`, `LICENSE.txt`, and `recipes/.../meta.yaml`.\nYou can configure this in a `tool.tyrannosaurus` section of `pyproject.toml`.\nFor an example, see [tyrannosaurus's own pyproject.toml](https://github.com/dmyersturnbull/tyrannosaurus/blob/master/pyproject.toml) file.\n\nThe information copied includes version, description, dependencies, and preferred line length.\nAlways generates backups under `.tyrannosaurus` before modifying.\nYou can clear this and other temp files with `tyrannosaurus clean`.\n\nProjects are configured for:\n- Build: Poetry, Tox, Conda, DepHell, Travis\n- Style: Black, Coverage, MyPy, Flake8, pycodestyle, pydocstyle, EditorConfig, pre-commit-hooks\n- Documentation: ReadTheDocs, Sphinx, Napoleon, autodoc, viewcode\n- Deploy: wheels, sdist, Twine, Docker, Conda-Forge\n\n[Poetry](https://github.com/python-poetry/poetry) is fantastic and highly recommended.\nAlso see [DepHell](https://github.com/dephell/dephell) and [conda-forge](https://conda-forge.org/).\n\n### Building, extending, and contributing\n\n[New issues](https://github.com/dmyersturnbull/tyrannosaurus/issues) and pull requests are welcome.\n\nTyrannosaurus is licensed under the [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\nThe author wrote it after making 18 Git commits trying to configure readthedocs, PyPi, and Tox.\nThis avoids that struggle for 99% of projects.\n\nConda build:\n1. `pip install m2-patch`\n2. `conda skeleton pypi tyrannosaurus`\n\n\n```\n                                              .++++++++++++.\n                                           .++HHHHHHH^^HHH+.\n                                          .HHHHHHHHHH++-+-++.\n                                         .HHHHHHHHHHH:t~~~~~\n                                        .+HHHHHHHHHHjjjjjjjj.\n                                       .+NNNNNNNNN/++/:--..\n                              ........+NNNNNNNNNN.\n                          .++++BBBBBBBBBBBBBBB.\n .tttttttt:..           .++BBBBBBBBBBBBBBBBBBB.\n+tt+.      ``         .+BBBBBBBBBBBBBBBBBBBBB+++cccc.\nttt.               .-++BBBBBBBBBBBBBBBBBBBBBB++.ccc.\n+ttt++++:::::++++++BBBBBBBBBBBBBBBBBBBBBBB+..++.\n.+TTTTTTTTTTTTTBBBBBBBBBBBBBBBBBBBBBBBBB+.    .ccc.\n  .++TTTTTTTTTTBBBBBBBBBBBBBBBBBBBBBBBB+.      .cc.\n    ..:++++++++++++++++++BBBBBB++++BBBB.\n           .......      -LLLLL+. -LLLLL.\n                        -LLLL+.   -LLLL+.\n                        +LLL+       +LLL+\n                        +LL+         +ff+\n                        +ff++         +++:\n                        ++++:\n```\n",
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/tyrannosaurus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
