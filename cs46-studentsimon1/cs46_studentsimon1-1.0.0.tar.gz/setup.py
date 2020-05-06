import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_studentsimon1",
    version="1.0.0",
    description="CSCI046 Data Structures Trees!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/studentsimon/trees",
    author="StudentSimon",
    author_email="email@cmc.edu",
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    install_requires=["pytest", "hypothesis"],
)
