# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['networkx_query']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.4,<3.0']

setup_kwargs = {
    'name': 'networkx-query',
    'version': '0.1.0',
    'description': 'NetworkX Query Tool',
    'long_description': '# networkx-query\n\n\n[![Unix Build Status](https://img.shields.io/travis/geronimo-iia/networkx-query/master.svg?label=unix)](https://travis-ci.com/geronimo-iia/networkx-query)[![Coverage Status](https://img.shields.io/coveralls/geronimo-iia/networkx-query/master.svg)](https://coveralls.io/r/geronimo-iia/networkx-query)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fe669a02b4aa46b5b1faf619ba2bf382)](https://www.codacy.com/app/geronimo-iia/networkx-query?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=geronimo-iia/networkx-query&amp;utm_campaign=Badge_Grade)[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/geronimo-iia/networkx-query.svg)](https://scrutinizer-ci.com/g/geronimo-iia/networkx-query/?branch=master)\n[![PyPI Version](https://img.shields.io/pypi/v/networkx-query.svg)](https://pypi.org/project/networkx-query)\n[![PyPI License](https://img.shields.io/pypi/l/networkx-query.svg)](https://pypi.org/project/networkx-query)\n\nVersions following [Semantic Versioning](https://semver.org/)\n\n## Overview\n\nNetworkX Query Tool (preview)\n\n## Installation\n\nInstall this library directly into an activated virtual environment:\n\n```text\n$ pip install networkx-query\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add networkx-query\n```\n\n## Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import networkx_query\n>>> networkx_query.__version__\n```\n\nSee [documentation](https://geronimo-iia.github.io/networkx-query).\n\n## Example\n\n',
    'author': 'Jerome Guibert',
    'author_email': 'jguibert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/networkx_query',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
