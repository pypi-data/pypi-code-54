from setuptools import setup
from ltplugins import __about__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(long_description=long_description, **__about__.about)
