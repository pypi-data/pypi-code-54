# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['a2wsgi']
setup_kwargs = {
    'name': 'a2wsgi',
    'version': '0.1.0',
    'description': 'Convert WSGI app to ASGI app.',
    'long_description': '# a2wsgi\n\nConvert WSGI app to ASGI app.\n\n## How to use\n\n```python\nfrom a2wsgi import WSGIMiddleware\n\nASGI_APP = WSGIMiddleware(WSGI_APP)\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/a2wsgi',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
