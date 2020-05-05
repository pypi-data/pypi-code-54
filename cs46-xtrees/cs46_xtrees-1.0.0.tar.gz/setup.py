import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_xtrees",
    version="1.0.0",
    description="Implementation of tree data structures, including BST, AVL and Heap, by xxing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/xxing21/trees",
    author="Xinran Xing",
    author_email="xxing21@cmc.edu",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    install_requires=["pytest", "hypothesis"],
)
