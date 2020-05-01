#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B.S.D.
Created on Wed Apr 29 10:01:43 2020

@author: Sara Ben Shabbat
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vpn_exclude_sbs",
    version="0.2.0",
    author="Sara Ben Shabbat",
    author_email="sarabenshabbat@gmail.com",
    description="A package for excluding DNSs from VPN connection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["vpn_exclude_sbs"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)


