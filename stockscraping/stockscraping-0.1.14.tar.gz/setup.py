# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stockscraping']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.0,<5.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'jupyterlab>=2.1.0,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pylint>=2.5.0,<3.0.0',
 'pysnooper>=0.4.0,<0.5.0',
 'yapf>=0.30.0,<0.31.0']

setup_kwargs = {
    'name': 'stockscraping',
    'version': '0.1.14',
    'description': '',
    'long_description': None,
    'author': 'akioyamada',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
