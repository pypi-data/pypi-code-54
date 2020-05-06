import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "lazybuild/README.md").read_text()

# This call to setup() does all the work
setup(
    name="lazybuild",
    version="1.0.0",
    description="A remote compiling tool for GameMaker Studio 2.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/imlazyeye/lazybuild",
    author="lazyeye",
    author_email="imlazyeye@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["lazybuild"],
    include_package_data=True,
    install_requires=["boto3", "paramiko", "termcolor", "colorama"],
    entry_points={
        "console_scripts": [
            "lazybuild = lazybuild.__main__:main",
        ]
    },
)