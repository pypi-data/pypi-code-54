import pathlib
from setuptools import find_packages,setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = ( HERE/"README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs_46_Curtis_working_trees",
    version="1.0.1",
    description="This package implements BST, AVL, and Heap.",
    long_description = README,
    long_description_content_type="text/markdown",
    url="https://github.com/CurtisSalinger/trees/tree/master",
    author="curtissalinger",
    author_email="csalinger22@cmc.edu",
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['Trees'],
    include_package_data=True,
    install_requires=["hypothesis", "pytest"],
    entry_points={
    },
)
