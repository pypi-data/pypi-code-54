# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['huntflow_py']

package_data = \
{'': ['*']}

install_requires = \
['email_validator>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['test = python3 -m doctest ./huntflow_py/*']}

setup_kwargs = {
    'name': 'huntflow-py',
    'version': '0.1.0',
    'description': 'Huntflow API library for Python',
    'long_description': "# Info\n\n## Requirements\n\nTo use [Huntflow API](https://github.com/huntflow/api) you need to obtain personal token by asking support via email.\n\nThis library also requires you to set proper (at least valid) email to let Huntflow staff contact you in case of emergency.\n\n## Usage\n\nAfter you're ready, usage is quite simple:\n\n```python\nfrom huntflow_py.api import APIv1 as Huntflow\n\nhuntflow = Huntflow(\n  token='your-token-here',\n  email='your-email-here',\n)\n\nprint(huntflow.me())\n```\n\nFor other methods see `api.py`.\n\nRight now I'm not sure how to generate available methods list automatically, feel free to contact and let me know.\n",
    'author': 'Kirill K',
    'author_email': 'kovalev.kirill.a@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agrrh/huntflow-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
