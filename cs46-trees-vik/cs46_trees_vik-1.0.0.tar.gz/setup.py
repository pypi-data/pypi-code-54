import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_trees_vik",
    version="1.0.0",
    description="Python code for tree data structures",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vik-jhun/trees",
    author="Vikramaditya Jhunjhunwala",
    author_email="vjhunjhunwala20@cmc.edu",
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    install_requires=["pytest", "hypothesis"],
)
