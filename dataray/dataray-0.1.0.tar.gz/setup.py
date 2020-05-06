# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataray', 'dataray.helper', 'dataray.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dataray',
    'version': '0.1.0',
    'description': 'a class of decorators helping inspect data',
    'long_description': '# DataRay\n\nDataRay is a class of decorators helping detect the metadata of the data.\n\nThe motivation of this package is to help understand how your api request data looks like. Normally we can directly\ncheck how the api request looks like via some UI platform such as postman etc. With this package, user may directly\nget the data structure and some basic metadata of the requested data\n\n## Features\n* Json Structure\n* Further feature coming soon\n\n\n## Detect the Json Structure\n\n```python\n# here is your customer request function. Now it is supposed to return list or dict you are interested in looking into\nfrom dataray import dataray\n\n@ dataray.ray()\ndef request_func():\n    ...\n```\nThen every time calling `request_func`, the json structure will be printed out.',
    'author': 'Zhen404',
    'author_email': 'zl2632@columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Zhen404/dataray',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
