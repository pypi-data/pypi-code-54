import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="teos-common",
    version="0.0.1",
    author="Sergi Delgado",
    author_email="sergi.delgado.s@gmail.com",
    description="Common library for The Eye of Satoshi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talaia-labs/python-teos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)