from os.path import normpath
from setuptools import setup, find_packages
from yaml_walker import __version__, __author__, __author_email__, __git_url__

with open(normpath('README.md'), 'r') as rm:
    long_description = rm.read()

setup(
    name='yaml_walker',
    version=__version__,
    packages=find_packages(),
    url=__git_url__,
    license='MIT',
    author=__author__,
    author_email=__author_email__,
    description='Data walker (in dot notation style) & filter (Xpath analog) for yaml look data structure',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=['PyYAML'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    package_data={
        '': [
            'unittests/*.yaml'
        ]
    }
)
