# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nrkdownload']

package_data = \
{'': ['*']}

install_requires = \
['future>=0.18.2,<0.19.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'requests_cache>=0.5.2,<0.6.0',
 'tqdm>=4.46.0,<5.0.0']

entry_points = \
{'console_scripts': ['nrkdownload = nrkdownload.commandline_script:main']}

setup_kwargs = {
    'name': 'nrkdownload',
    'version': '2.1.2',
    'description': 'Download series or programs from NRK, complete with images and subtitles',
    'long_description': '# nrkdownload\n![Supports python 2.7, 3.6, 3.7, 3.8](https://img.shields.io/badge/python-2.7%2C%203.6%2C%203.7%2C%203.8-brightgreen.svg "Supported Python versions")\n\nThis is a commandline tool to download programs and series from NRK (Norwegian public broadcaster). It supports both TV, Radio and Podcast content. The tool is written in Python, and is compatible with Python 2.7 and 3.x. It has been tested under Linux, Mac OS X and Windows.\n\n# Documentation\nThe documentation for nrkdownload is availabe here:\nhttps://nrkdownload.readthedocs.org\n\n# Setting up a development environment\nInstall [poetry](https://python-poetry.org/), and a recent Python version (>=3.6).\nIf you want to run tests with multiple Python versions, install [pyenv](https://github.com/pyenv/pyenv).\nSet up the development environment:\n```bash\npoetry install\n```\n\n\n# Making a new release\n- Make sure all tests are ok by running `tox`\n- Make a pull requst on GitHub\n- Use the "new release" functionallity of GitHub. Make a new tag.\n- Update `pyproject.toml` to match the new version number.\n- `poetry build`\n- `poetry publish`\n',
    'author': 'Martin Høy',
    'author_email': 'marhoy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marhoy/nrk-download',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
