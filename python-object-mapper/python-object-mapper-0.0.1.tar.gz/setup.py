"""Setup script for python-object-mapper"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="python-object-mapper",
    version="0.0.1",
    description="Python Object Mapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/python-object-mapper/python-object-mapper",
    author="Python Object Mapper",
    author_email="maxim@derbin.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["pyom"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)
