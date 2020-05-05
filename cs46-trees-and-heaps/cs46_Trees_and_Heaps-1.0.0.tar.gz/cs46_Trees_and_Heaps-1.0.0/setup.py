import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_Trees_and_Heaps",
    version="1.0.0",
    description="Class Structures for implementing binary trees, avl trees, and heaps",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/maryaornelas/trees",
    author="Marya Ornelas",
    author_email="maryaornelas@gmail.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["trees"],
    install_requires=["pytest", "hypothesis"],
)
