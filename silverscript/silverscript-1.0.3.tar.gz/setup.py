#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 13:05:04 2020

@author: augustinjose
"""


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="silverscript", # Replace with your own username
    version="1.0.3",
    author="Augustin Jose",
    author_email="augustinjose1221@gmail.com",
    description=" Silver is a customizable python based shell prompt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AugustinJose1221/silver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['silver/silver.py']
)

