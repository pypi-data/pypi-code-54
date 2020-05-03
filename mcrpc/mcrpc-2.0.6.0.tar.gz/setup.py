# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcrpc']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.3,<2.0.0',
 'configobj>=5.0.6,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'simplejson>=3.17.0,<4.0.0']

setup_kwargs = {
    'name': 'mcrpc',
    'version': '2.0.6.0',
    'description': 'mcrpc: MultiChain RPC Library',
    'long_description': '# mcrpc - Multichain RPC client\n\n[![Version](https://img.shields.io/pypi/v/mcrpc.svg)](https://pypi.python.org/pypi/mcrpc/)\n[![Downloads](https://pepy.tech/badge/mcrpc)](https://pepy.tech/project/mcrpc)\n\n\n## Content Blockchain RPC Client\n\nA Python 3 MultiChain RPC client built for the \n[Content Blockchain Project](https://content-blockchain.org/)\n\nThe versioning scheme follows [MultiChain](https://www.multichain.com/download-community/)\nand includes code generated function annotations and api documentation to support code \ncompletion and get you up to speed fast.\n\n\n## Code Completion\n\n![mcrpc code completaion](https://raw.githubusercontent.com/coblo/mcrpc/master/images/mcrpc_cc.png)\n\n\n## Code Documentation\n\n![mcrpc documentation](https://raw.githubusercontent.com/coblo/mcrpc/master/images/mcrpc_doc.png)\n\n\n## Installing\n\nThe RPC client is published with the package name [mcrpc](https://pypi.python.org/pypi/mcrpc) \non Python Package Index. Install it with:\n\n```console\n$ pip3 install mcrpc\n```\n\n## Usage\n\nIf you have a local blockchain node with default data-dir you can do:\n\n```python\nimport mcrpc\n\nclient = mcrpc.autoconnect()\nclient.getinfo()\n```\n\n## Change Log\n\n### 2.0.6.0 (2020-05-03)\n- Add autoconnect convenience function\n- Switched package versioning to match multichain\n- Switched to poetry based packaging\n- Updated to multichain node 2.0.6\n\n\n### 1.0.2 (2019-02-13)\n- Fix signature of appendrawexchange and completerawexchange\n- Build rpc client against Multichain 2 Beta 2\n- Add pretty-print support for response objects\n- Sort response class properties for cleaner diffs on updates\n',
    'author': 'titusz',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coblo/mcrpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
