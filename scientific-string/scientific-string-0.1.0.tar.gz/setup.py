import sys

from setuptools import setup

PY3 = sys.version_info

if PY3 < (3, 5):
    raise EnvironmentError(
        'Please use CPython interpreter higher than version 3.5!')

setup(
    name='scientific-string',
    version='0.1.0',
    packages=['scientific_string'],
    url='https://github.com/singularitti/scientific-string',
    license='MIT',
    author='Qi Zhang',
    author_email='qz2280@columbia.edu',
    description='A Python toolkit dealing with daily strings in scientific research.'
)
