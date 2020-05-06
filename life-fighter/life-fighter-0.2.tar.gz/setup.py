# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['life_fighter', 'life_fighter.extra', 'life_fighter.extra.old']

package_data = \
{'': ['*'],
 'life_fighter': ['data/*',
                  'data/cells/conway/*',
                  'data/cells/games/*',
                  'data/fonts/*',
                  'data/imgs/*',
                  'data/imgs/backgrounds/*',
                  'data/music/*',
                  'data/sounds/*',
                  'data/texts/*']}

install_requires = \
['pygame>=2.0.0.dev8,<3.0.0']

setup_kwargs = {
    'name': 'life-fighter',
    'version': '0.2',
    'description': 'Variante del Juego de la Vida de Conway para un jugador',
    'long_description': None,
    'author': 'Juanjo Conti',
    'author_email': 'jjconti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jjconti/life-fighter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
