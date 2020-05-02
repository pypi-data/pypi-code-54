import setuptools
from pathlib import Path

setuptools.setup(
    name="devalpdf",
    version=1.0,
    long_descripetion=Path("README.MD").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])

)
