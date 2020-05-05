# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ln', 'test_ln']
entry_points = \
{'console_scripts': ['lnp = ln:main']}

setup_kwargs = {
    'name': 'ln.py',
    'version': '1.0.0',
    'description': 'symlinks made easier',
    'long_description': 'ln.py\n=====\n\n.. image:: http://img.shields.io/pypi/v/ln.py.png\n  :target: https://pypi.python.org/pypi/ln.py\n\nYou always get ``ln`` arguments in the wrong order?\n\nThen ``ln.py`` is for you.\n\nInstallation\n-------------\n\n``pip3 install ln.py``\n\nAPI\n---\n\nInstead of cryptic ``os.symlink(src, dest)``, use :\n``ln.ln(from_=first, to=second)``\n\nDemo\n-----\n\nSee ``lnp`` demo on `asciinema.org <https://asciinema.org/a/101084>`_\n',
    'author': 'Dimitri Merejkowsky',
    'author_email': 'd.merej@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmerejkowsky/ln.py',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
