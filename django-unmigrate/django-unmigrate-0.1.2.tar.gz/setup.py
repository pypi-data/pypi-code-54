# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_unmigrate',
 'django_unmigrate.management',
 'django_unmigrate.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.0,<4.0', 'gitpython>=3.1.1,<4.0.0']

setup_kwargs = {
    'name': 'django-unmigrate',
    'version': '0.1.2',
    'description': 'Smart reversion of Django migrations based on Git diff',
    'long_description': "django-unmigrate\n================\n\n.. image:: https://img.shields.io/badge/packaging-poetry-purple.svg\n    :alt: Packaging: poetry\n    :target: https://github.com/sdispater/poetry\n\n.. image:: https://img.shields.io/badge/code%20style-black-black.svg\n    :alt: Code style: black\n    :target: https://github.com/ambv/black\n\n.. image:: https://badges.gitter.im/Join%20Chat.svg\n    :alt: Join the chat at https://gitter.im/django-unmigrate\n    :target: https://gitter.im/django-unmigrate/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link\n\n.. image:: https://github.com/lorinkoz/django-unmigrate/workflows/code/badge.svg\n    :alt: Build status\n    :target: https://github.com/lorinkoz/django-unmigrate/actions\n\n.. image:: https://coveralls.io/repos/github/lorinkoz/django-unmigrate/badge.svg?branch=master\n    :alt: Code coverage\n    :target: https://coveralls.io/github/lorinkoz/django-unmigrate?branch=master\n\n.. image:: https://badge.fury.io/py/django-unmigrate.svg\n    :alt: PyPi version\n    :target: http://badge.fury.io/py/django-unmigrate\n\n.. image:: https://img.shields.io/pypi/dm/django-unmigrate\n    :alt: Downloads\n\n|\n\nIf you are in a complex Django project, sometimes you will find yourself switching\nbetween multiple branches, some of which can add a number of database migrations.\nBefore switching back to ``master`` you will have to unapply all migrations that\nare specific to the current branch. To make things worse, in order to unapply\nDjango migrations, you have to enter the migration that comes right before the\nfirst migration of the current branch. It's not that big of a deal, Django is\nsmart enough to let you use an unambiguos prefix of any migration, but with\nthis package you can speed things up a little bit.\n\nWhile standing on any branch, you can use::\n\n    python manage.py unmigrate master\n\nOr if it's going to be ``master`` anyways, this will suffice::\n\n    python manage.py unmigrate\n\nAnd that's it!\n\nA little deeper\n---------------\n\nOk, you can do more than that.\n\nDo you need to unapply your migrations from the same branch, a few commits\nbehind? Here's how::\n\n    python manage.py unmigrate HEAD~5\n    python manage.py unmigrate af332b\n    python manage.py unmigrate v1.33.7\n\nIf you only want to see the target migrations::\n\n    python manage.py unmigrate --dry-run\n\nAnd if you just want to play with this, go ahead and unapply your migrations\nwith ``fake``. Just don't forget to apply them again::\n\n    python manage.py unmigrate --fake\n    python manage.py migrate --fake\n\n\nContributing\n------------\n\n- Join the discussion at https://gitter.im/django-unmigrate/community.\n- PRs are welcome! If you have questions or comments, please use the link\n  above.\n- To run the test suite run ``make`` or ``make coverage``. The tests for this\n  project live inside a small django project called ``dunm_sandbox``. Beware!\n  This package uses Git to function, therefore, the tests expect a number of\n  commit hashes inside this repository to remain stable in order to function.\n  See `this meta file`_ for further details.\n\n.. _this meta file: dunm_sandbox/meta.py\n",
    'author': 'Lorenzo Peña',
    'author_email': 'lorinkoz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lorinkoz/django-unmigrate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
