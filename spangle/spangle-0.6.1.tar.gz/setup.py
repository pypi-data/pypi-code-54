# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spangle', 'spangle.cli', 'spangle.models']

package_data = \
{'': ['*']}

install_requires = \
['addict>=2.2.1,<3.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'asgiref>=3.2.3,<4.0.0',
 'chardet>=3.0.4,<4.0.0',
 'httpx>=0.12.0,<0.13.0',
 'jinja2>=2.10.3,<3.0.0',
 'multidict>=4.7.3,<5.0.0',
 'multipart>=0.2,<0.3',
 'parse>=1.14.0,<2.0.0',
 'starlette==0.13.2',
 'urllib3>=1.25.7,<2.0.0']

entry_points = \
{'console_scripts': ['spangle = spangle.cli.run:main']}

setup_kwargs = {
    'name': 'spangle',
    'version': '0.6.1',
    'description': 'ASGI apprication framework inspired by `responder`, `vibora`, and `express-js`.',
    'long_description': '# spangle \n\n[![PyPI](https://img.shields.io/pypi/v/spangle)](https://pypi.org/project/spangle/)\n[![PyPI - License](https://img.shields.io/pypi/l/spangle)](https://pypi.org/project/spangle/)\n\nASGI application framework inspired by [responder](https://github.com/taoufik07/responder), [vibora](https://github.com/vibora-io/vibora), and [express-js](https://github.com/expressjs/express/). \n\n\nNote: `spangle` is on pre-alpha stage, so any updates may contain breaking changes.\n\n## Getting Started\n\n### Install\n\n```shell\npip install spangle\npip install hypercorn # or your favorite ASGI server\n```\n\n### Hello world\n\n```python\n# hello.py\nimport spangle\n\napi = spangle.Api()\n\n@api.route("/")\nclass Index:\n    async def on_request(self, req, resp):\n        resp.set_status(418).set_text("Hello world!")\n        return resp\n\n```\n\n```shell\nhypercorn hello:api\n```\n\n## Features\n\n* Component (from `vibora`!)\n* Flexible url params\n* `Jinja2` built-in support\n* Uniformed API\n* Single page application friendly\n\n...and more features. See [documents](http://tkamenoko.github.io/spangle).\n\n\n## Contribute\n\nContributions are welcome!\n\n* New features\n* Bug fix\n* Documents\n\n\n### Prerequisites\n\n* Python>=3.7\n* git\n* poetry\n* yarn\n\n### Build\n\n```shell\n# clone this repository.\ngit clone http://github.com/tkamenoko/spangle.git \n# install dependencies.\npoetry install\nyarn install\n```\n\n### Test\n\n```shell\nyarn test\n```\n\n### Update API docs\n\n```shell\nyarn doc:build\n```\n',
    'author': 'T.Kameyama',
    'author_email': 'tkamenoko@vivaldi.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tkamenoko/spangle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
