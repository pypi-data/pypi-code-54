# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['with_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'with-utils',
    'version': '0.2.1',
    'description': 'WITH utils',
    'long_description': "With Utils\n==========\n\nUtils that we've used a lot at WITH.\n\n## `iter`\n\nIteration-related utils\n\n### `n_grams`\n\nProvides a way to create n_grams from an iterator\n\n```python\nfrom with_utils.iter import n_grams\nassert list(n_grams([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]\n```\n\n### `return_list`\n\nTransforms an iterator into a function that returns a list.\n\n```python\nfrom with_utils.iter import return_list\n\n@return_list\ndef foo():\n    yield 1\n    yield 2\n    yield 3\n\nassert foo() == [1, 2, 3]\n```\n",
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@with-madrid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WithIO/with-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
