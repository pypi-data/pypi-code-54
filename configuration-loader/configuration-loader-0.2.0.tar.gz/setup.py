# -*- coding: utf-8 -*-

"""Python configuration loader."""

import os

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

install_require = []

setup_require = [
    'pytest-runner>=2.6.2',
]

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'mock>=2.0.0',
    'pydocstyle>=1.0.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

extras_require = {
    'docs': ['Sphinx>=3.0.3',],
    'tests': tests_require,
    'dev': ['ipdb', 'black'],
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('config_loader', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']


setup(
    author="Esteban J. G. Gabancho",
    author_email='egabancho@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description=__doc__,
    install_require=install_require,
    extras_require=extras_require,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='configuration config loader',
    name='configuration-loader',
    packages=find_packages(),
    setup_requires=setup_require,
    test_suite='tests',
    tests_require=tests_require,
    url='https://github.com/egabancho/config-loader',
    version=version,
    zip_safe=False,
)
