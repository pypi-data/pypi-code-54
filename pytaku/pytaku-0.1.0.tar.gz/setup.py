# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytaku']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.5,<4.0.0', 'goodconf>=1.0.0,<2.0.0', 'psycopg2>=2.8.5,<3.0.0']

entry_points = \
{'console_scripts': ['pytaku-generate-config = pytaku:generate_config',
                     'pytaku-generate-psql-envars = '
                     'pytaku:generate_psql_envars',
                     'pytaku-manage = pytaku:manage']}

setup_kwargs = {
    'name': 'pytaku',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Bùi Thành Nhân',
    'author_email': 'hi@imnhan.com',
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
