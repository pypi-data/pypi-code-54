"""Setup script for realpython-second"""

import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="lmbr-second",
    version="1.0.2",
    description="Read the latest - lmbr",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/second",
    author="Lmbr",
    author_email="lmbr@lmbr.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "lmbr-reader",
    ],
    entry_points={"console_scripts": ["realpython=second.__main__:main"]},
)
