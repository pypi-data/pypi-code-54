#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    'pytest'
]

setup(
    name='insensitive-dict',
    version='1.0.0',
    description="A case insensitive dictionary that's fully tested.  Primarily broken out from the requests package",
    long_description=readme + '\n\n' + history,
    author="Tim Martin",
    author_email='tim@timmartin.me',
    url='https://github.com/timmmartin19/case_insensitive_dict',
    py_modules=['insensitive_dict'],
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='case_insensitive_dict',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='insensitive_dict_tests',
    tests_require=test_requirements
)
