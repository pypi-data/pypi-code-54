import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_python_trees_gloriachoi",
    version="1.0.0",
    description="Python tree implementations of Binary Tree, BST, Heaps, and AVL",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gloriachoi99/trees",
    author="Gloria Choi",
    author_email="gchoi99@gmail.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    install_requires=["pytest", "hypothesis"],
    )
