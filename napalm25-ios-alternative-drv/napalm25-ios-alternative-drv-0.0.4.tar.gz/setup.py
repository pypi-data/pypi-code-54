from setuptools import setup, find_packages
from os import path
import sys

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

lpath = path.abspath(path.dirname(__file__))

with open(path.join(lpath, 'README.md'), encoding='utf-8') as fh:
    long_description = fh.read()

with open(path.join(lpath, 'requirements.txt'), "r") as fh:
    reqs = [r for r in fh.read().splitlines() if len(r) > 0]

setup(
    name='napalm25-ios-alternative-drv',
    version='0.0.4',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    py_modules=['ios_ad'],
    url='https://github.com/remingu/napalm-ios-ad',
    license='Apache 2.0',
    author='Daniel Schlifka(remingu)',
    author_email='Daniel Schlifka <remingu@techturn.de>',
    description='[obsolete with Napalm3] alternative driver plugin for cisco ios',
    install_requires=reqs,
    keywords='development napalm ios  ',
    python_requires='>=3.6',
    project_urls={
        'Bug Reports': 'https://github.com/remingu/napalm-ios-ad/issues',
        'Source': 'https://github.com/remingu/napalm-ios-ad',
    },
    include_package_data=True,
)
