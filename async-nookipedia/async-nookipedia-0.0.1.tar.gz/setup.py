# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nookipedia', 'nookipedia.api', 'nookipedia.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'importlib_metadata>=1.6.0,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'async-nookipedia',
    'version': '0.0.1',
    'description': 'async API wrapper for Nookipedia API written in python',
    'long_description': '# async-nookipedia\nAsync API wrapper for Nookipedia API utilizing the [aiohttp](https://docs.aiohttp.org/en/stable/) package.\n\n## Beta\nThis package is currently in beta and not yet fully finished. \n\n## Installation\nasync-nookipedia can be installed via pip.\n\n`pip install async-nookipedia`\n\n## Documentation\n\nProper docs are coming soon!\n\n## Usage\n```python\nimport asyncio\nfrom nookipedia import Nookipedia\n\n\napi_key = "API_KEY"\n\nasync def main():\n    api = Nookipedia(api_key=api_key, cached_api=True)\n    villager = await api.get_villager(\'marshal\')\n    print(villager.name)\n    critter = await api.get_critter(\'spider\')\n    print(critter.name)\n    fossil = await api.get_fossil(\'amber\')\n    print(fossil.name)\n\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n\n# Requirements\n- Python >= 3.6\n- [aiohttp](https://docs.aiohttp.org/en/stable/)\n- [python-dateutil](https://dateutil.readthedocs.io/en/stable/) \n- [importlib_metadata](https://importlib-metadata.readthedocs.io/en/latest/)\n\n# Issues and Features\nIf you\'re having any issues or want additional features please create an Issue on [github](https://github.com/makupi/async-nookipedia/issues).\n\n[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A015HXK)',
    'author': 'makubob',
    'author_email': 'makupi@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/makupi/async-nookipedia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
