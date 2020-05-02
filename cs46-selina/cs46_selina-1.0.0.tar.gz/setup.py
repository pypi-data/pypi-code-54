import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_selina",
    version="1.0.0",
    description="provides code to implement binary trees, binary search trees, avl trees, and heaps",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/selina-28030/trees",
    author="Selina Ho",
    author_email="selina28030@gmail.com",
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["trees"],
    include_package_data=False,
    install_requires=["pytest", "hypothesis"],
)
