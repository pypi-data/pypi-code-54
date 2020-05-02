# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_pwa']

package_data = \
{'': ['*'],
 'flask_pwa': ['static/*',
               'static/images/*',
               'static/images/icons/*',
               'static/js/*',
               'templates/pwa/*']}

install_requires = \
['flask>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'flask-pwa',
    'version': '0.1.0',
    'description': 'Extends your Flask app into a PWA.',
    'long_description': '# Flask-PWA\n\n![Python package](https://github.com/pacotei/flask-pwa/workflows/Python%20package/badge.svg)\n\nA extension to give a PWA experience into your Flask web application.\nThis extension provide some files to give your app some PWA experience like app installation, cached files and offline page.\n\n### Requires:\n - Flask\n - Jinja\n\n### Installation:\nTo use Flask-PWA extension in your project you need to install it with pip.\n\n```bash\npip install flask-pwa\n```\n\n### How it works\nFlask-PWA provide some configuration files into your app: ```manifest.json```, ```sw.js```, ```offline.html``` and ```icons```, to deliver best PWA experience.  \nPWA use this files to configure the minimum environment to works.\n',
    'author': 'bergpb',
    'author_email': 'lindembergdepaulo@@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pacotei/flask-pwa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
