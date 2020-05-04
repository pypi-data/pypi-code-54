from setuptools import setup

def readme():
    with open("README.md") as file:
        README = file.read()
    return README

setup(
name="winpip",
version="1.0",
description="This Lets the windows interpreter programmer to manage pip commands in python programme",
long_description=readme(),
long_description_content_type ='text/markdown',
url="https://github.com/GaneshKaricharla2000/win-pip",
author="Karicharla GNV Swamy Naidu",
author_email="ganeshkaricherla@gmail.com",
license ="MIT",
classifiers=[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python"
],
packages=["win_pip"],
include_package_data=True
)