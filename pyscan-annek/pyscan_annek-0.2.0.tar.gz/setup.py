# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyscan_annek']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'pywinrm>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['pyscan = pyscan_annek.cli:main']}

setup_kwargs = {
    'name': 'pyscan-annek',
    'version': '0.2.0',
    'description': 'Scan for hosts and identify',
    'long_description': None,
    'author': 'Michael MacKenna',
    'author_email': 'mpmackenna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
