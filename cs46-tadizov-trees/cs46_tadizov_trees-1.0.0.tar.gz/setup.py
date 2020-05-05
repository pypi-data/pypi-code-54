import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_tadizov_trees",
    version="1.0.0",
    description="cs46 Implementation of BST AVL and Heap",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tadizov/trees",
    author="Timur",
    author_email="timadizov@gmail.com",
    license="GPLv3",
    classifiers=[
        
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    include_package_data=False,
    install_requires=["pytest", "hypothesis"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
