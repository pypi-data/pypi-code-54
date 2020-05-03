import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="wintemp",
    version="1.0.0",
    description="Remove Windows Temporary Files",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Arjun Basandrai",
    author_email="arjunbasandrai2004@gmail.com",
    packages=['wintemp'],
)