#!/usr/bin/env  python
# encoding utf-8

"""
Setup file to create pypi package for auto_self_params.
"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="auto_self_params",
    version="0.0.1",
    author="Steve Barmes",
    author_email="gadgetsteve@hotmail.com",
    license='MIT License',
    description="Automatic creation of self properties from parameters.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/GadgetSteve/auto_self_params",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.6',
)
