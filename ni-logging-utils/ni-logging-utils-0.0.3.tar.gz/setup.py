import setuptools

from version import get_git_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ni-logging-utils", # Replace with your own username
    version=get_git_version(),
    author="Primael Bruant",
    author_email="primael.bruant@gmail.com",
    description="A small tools to log",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/naturalinterface/logging_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
