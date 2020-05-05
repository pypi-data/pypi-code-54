import re

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
package = 'sanic_jwt_payload_encrypt'

with open(path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(path.join(here, package, '__init__.py')) as f:
    version = re.search(
        r'(__version__)([\s]*=[\s]*\")([\d\.]+)', f.read()
    ).group(3)

setup(
    version=version,
    install_requires=required,
)