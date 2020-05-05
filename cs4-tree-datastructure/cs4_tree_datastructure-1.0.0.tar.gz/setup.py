import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs4_tree_datastructure",
    version="1.0.0",
    description="Implemenation of BST, AVL and Heap",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rayegleekel/trees",
    author="Raye Gleekel",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    include_package_data=True,
)
