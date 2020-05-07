import os

from distutils.core import setup
from configuration import ROOT_DIR

with open(os.path.join(ROOT_DIR, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name='wwexercise',
    version='v0.5',
    description='Weight Watchers coding exercise in python',
    url='https://github.com/birdman0030/wwexercise',
    author='Kurt Bird',
    author_email='kurtbird1@gmail.com',
    license='GNU',
    packages=['wwexercise'],
    install_requires=['selenium==3.141.0',
                      'pytest==5.4.1',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        ],
)
