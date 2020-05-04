#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.1.2',
    ]

setup_requirements = [
    'pytest-runner',
    ]

test_requirements = [
    'pytest>=3',
    ]

setup(
    author="Harsh Parekh",
    author_email='h.x.dev@outlook.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python library to compute a fuzzy time difference.",
    entry_points={
        'console_scripts': [
            'fuzzy_delta_time=fuzzy_delta_time.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fuzzy_delta_time',
    name='fuzzy_delta_time',
    packages=find_packages(include=['fuzzy_delta_time', 'fuzzy_delta_time.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hXtreme/fuzzy_delta_time',
    version='0.0.4',
    zip_safe=False,
)
