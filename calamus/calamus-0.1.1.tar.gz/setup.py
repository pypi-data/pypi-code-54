# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calamus']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.5.1,<4.0.0', 'pyld>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'calamus',
    'version': '0.1.1',
    'description': 'calamus is a library built on top of marshmallow to allow (de-)Serialization of Python classes to Json-LD.',
    'long_description': '..\n    Copyright 2017-2020 - Swiss Data Science Center (SDSC)\n    A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and\n    Eidgenössische Technische Hochschule Zürich (ETHZ).\n\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n\n.. image:: https://github.com/SwissDataScienceCenter/calamus/blob/master/docs/reed.png?raw=true\n   :scale: 50\n   :align: center\n\n==================================================\n calamus: Json-LD Serialization Libary for Python\n==================================================\n\ncalamus is a library built on top of marshmallow to allow (de-)Serialization\nof Python classes to Json-LD\n',
    'author': 'Swiss Data Science Center',
    'author_email': 'contact@datascience.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SwissDataScienceCenter/calamus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
