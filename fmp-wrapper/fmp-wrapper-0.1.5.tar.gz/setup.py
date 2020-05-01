from setuptools import setup, Command
import os

# Package meta-data.
NAME = 'fmp-wrapper'
DESCRIPTION = 'A python wrapper for the Financial Modeling Prep API.'
URL = 'https://github.com/cccdenhart/fmp-wrapper'
EMAIL = 'cccdenhart@me.com'
AUTHOR = 'Charlie Denhart'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.5'
proj_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(proj_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# What packages are required for this module to be executed?
REQUIRED = [
    'pandas'
]

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
    version=VERSION,
    py_modules=['fmp_wrapper'],
    url=URL,
    license='MIT'
)
