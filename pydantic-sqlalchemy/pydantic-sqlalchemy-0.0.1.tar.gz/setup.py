# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.5.1,<2.0.0', 'sqlalchemy>=1.3.16,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.6.0,<2.0.0']}

setup_kwargs = {
    'name': 'pydantic-sqlalchemy',
    'version': '0.0.1',
    'description': 'Tools to convert SQLAlchemy models to Pydantic models',
    'long_description': '# Pydantic-SQLAlchemy\n\nTools to generate Pydantic models from SQLAlchemy models.\n\nStill experimental.\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Sebastián Ramírez',
    'author_email': 'tiangolo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
