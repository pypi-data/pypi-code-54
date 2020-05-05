import setuptools
from pathlib import Path

setuptools.setup(
    name="pdfcreatormarian",
    version=1.0,
    long_description=Path("README.md").read_text(),#Reference long description to contents of readme file
    packages=setuptools.find_packages(exclude=["tests","data"])
    #Tell what packages will be distributed. Will automaticall discover packages. Exclude two directories which don`t include sourcecode.
)