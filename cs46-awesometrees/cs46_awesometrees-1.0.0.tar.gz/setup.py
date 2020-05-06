import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_awesometrees",
    version="1.0.0",
    description="Include AVL, BST, HEAP, all those popular and must knowndata structures. From a CMC CS46 class:https://github.com/mikeizbicki/cmc-csci046",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/StellaLX99/trees",
    author="Stella Li",
    author_email="stelli@students.pitzer.edu",
    license="GPL3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    install_requires=["pytest", "hypothesis"],
)
