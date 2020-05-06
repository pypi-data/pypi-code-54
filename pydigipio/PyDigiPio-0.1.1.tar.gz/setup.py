from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="PyDigiPio",
    version="0.1.1",
    description="Python module for Raspberry Pi GPIO",
    long_description=readme,
    author="Einar Arnason",
    author_email="einsiarna@gmail.com",
    url="https://github.com/EinarArnason/PyDigiPio",
    license=license,
    py_modules=["PyDigiPio"],
    test_suite="tests",
    platforms=["linux"],
)
