# -*- coding: utf-8 -*-
"""
setup.py
------------
learn-flow setup script.
TODO: change the framework name to Flow/Soul
"""
from setuptools import setup, find_packages
# builds the project dependency list
install_requires = None
with open('requirements.txt', 'r') as f:
    install_requires = f.readlines()

# setup function call
setup(
    name="simple-configuration",
    version="1.0.0",
    author="Luis Felipe Muller",
    author_email="luisfmuller@gmail.com",
    description=("A simple and lightweight config parser and handler."),
    keywords="config, settings, config parser",
    # Install project dependencies
    install_requires=install_requires,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md', "*.json", "*.zip"],
    },
    include_package_data=True,
    packages=find_packages(exclude=["*tests"]),
)
