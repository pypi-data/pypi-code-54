import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="argparsethis",
    version="1.1.1",
    author="TheTwitchy",
    author_email="the.twitchy@gmail.com",
    description="A drop-in replacement to Python's built-in argparse, that provides the capability to argparse any arbitrary string, not just command line arguments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/TheTwitchy/argparsethis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)