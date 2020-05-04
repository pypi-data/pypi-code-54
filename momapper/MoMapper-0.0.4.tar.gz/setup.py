# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['momapper', 'momapper.mongodb']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=3.10.1,<4.0.0']

setup_kwargs = {
    'name': 'momapper',
    'version': '0.0.4',
    'description': 'Python Mapper for MongoDB models',
    'long_description': '=======================\nMoMapper (Mongo Mapper)\n=======================\n\nPython Mapper for MongoDB models\n\n\n.. image:: https://img.shields.io/pypi/v/momapper.svg\n    :target: https://pypi.python.org/pypi/momapper\n\n.. image:: https://img.shields.io/travis/OvalMoney/momapper.svg\n    :target: https://travis-ci.org/OvalMoney/momapper\n\nFeatures\n--------\n\n* Schema validation for documents.\n* Type validation for document fields.\n* 100% compatible with Pymongo API.\n* Implements Mapper_ design pattern, separating schema and type validation from storage logic.\n\nInstallation:\n-------------\n\n.. code-block:: console\n\n    $ pip install momapper\n\nUsage:\n------\n\nCheck it out in the doc_.\n\nLicense\n-------\n\nFree software: MIT_ license.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`wboxx1/cookiecutter-pypackage`: https://github.com/wboxx1/cookiecutter-pypackage-poetry\n.. _MIT: ./LICENSE\n.. _Mapper: https://en.wikipedia.org/wiki/Data_mapper_pattern\n.. _doc: ./docs/usage.rst\n',
    'author': 'Walter Danilo Galante',
    'author_email': 'walter.galante@ovalmoney.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devilicecream/MoMapper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
