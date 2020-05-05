import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_trees_data_structure",
    version="1.0.0",
    description="This is a simple tree data structure implementation in Python covering Binary Search Trees, AVL Trees and Heaps.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/shashankvineet/trees",
    author="Shashank Vineet",
    author_email="shashankvineet98@gmail.com",
    license="GPLv3",
    classifiers=[
       # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    #include_package_data=True,
    install_requires=["pytest", "hypothesis"],
)
