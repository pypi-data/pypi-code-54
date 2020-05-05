"""Setup script for robolytix"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robolytix",
    version="0.1.0",
    author="Ondrej Fiala",
    author_email="ondrej.fiala@robolytix.com",
    description="Robolytix is the key online analytic and monitoring tool for Business / Robotic Process Automation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robolytix/robolytix-sdk/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)