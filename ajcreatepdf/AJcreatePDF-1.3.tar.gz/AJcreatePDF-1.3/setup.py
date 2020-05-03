import setuptools
from pathlib import Path


setuptools.setup(
    name="AJcreatePDF",
    version=1.3,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)                                                           # find_packages excude the given list of modules as they are not part of the source code
