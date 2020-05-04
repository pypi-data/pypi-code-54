import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_abundanceoftrees",
    version="3.0.3",
    description="Implementation of Binary Tree, AVL Tree and Heap Tree Data Structures",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ma-alvarado/trees",
    author="Matías Alvarado",
    author_email="matias@4alvarados.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    include_package_data=True,
    install_requires=["pytest", "hypothesis"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)

