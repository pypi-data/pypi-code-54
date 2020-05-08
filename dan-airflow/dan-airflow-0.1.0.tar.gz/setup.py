import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'dan_airflow', '_project.py')).read())
exec(open(os.path.join(here, 'dan_airflow', '_version.py')).read())
PACKAGE_NAME = __project__  # NOQA
VERSION = __version__  # NOQA
DEVELOPMENT_STATUS = "1 - Alpha"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

EXTRAS = {}
REQUIRES = []
with open('requirements.txt') as f:
    for line in f:
        line, _, _ = line.partition('#')
        line = line.strip()
        if ';' in line:
            requirement, _, specifier = line.partition(';')
            for_specifier = EXTRAS.setdefault(':{}'.format(specifier), [])
            for_specifier.append(requirement)
        else:
            REQUIRES.append(line)

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# if os.environ.get('CI_COMMIT_TAG'):
#     VERSION = os.environ['CI_COMMIT_TAG']
# else:
#     VERSION = os.environ['CI_JOB_ID']

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description='Airflow plugins for Dan Conger',
    author_email="",
    author="Dan Conger",
    license="Apache License Version 2.0",
    keywords=['airflow'],
    install_requires=REQUIRES,
    extras_require=EXTRAS,
    packages=['dan_airflow', 'dan_airflow.operators'],
    include_package_data=True,
    long_description=LONG_DESCRIPTION
)
