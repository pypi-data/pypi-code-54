import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_laky_trees",
    version="1.0.0",
    description="This is a tree data structure implementation in Python covering Binary Search Trees, AVL Trees and Heaps.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lakyli0818/trees",
    author="Laky Li",
    author_email="zli21@cmc.edm",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    install_requires=["pytest", "hypothesis"],
)
