from setuptools import setup
from setuptools import find_packages

setup(
    name='pytonic',
    version='0.0.1.dev1',
    python_requires='>=3.5',
    packages=find_packages(include=['pytonic']),
    author='Caio Amaral',
    author_email='caioaamaral@gmail.com',
    maintainer='Caio Amaral',
    maintainer_email='caioaamaral@gmail.com',
    url='https://github.com/caioaamaral/pytonic',
    entry_points={
        'console_scripts' : [
            'pytonic=pytonic.console:main'
        ],
        'pytonic.verbs':[
            'make = pytonic.verbs.pytonic_make'
        ]
    }
)
