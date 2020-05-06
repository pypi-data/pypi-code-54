import os
import shutil
import setuptools


with open("teos/common/README.md", "r") as fh:
    long_description = fh.read()

with open('teos/common/requirements.txt') as f:
    requirements = [r for r in f.read().split('\n') if len(r)]


# Remove undesired files
if os.path.exists("teos/common/__pycache__"):
    shutil.rmtree("teos/common/__pycache__")
if os.path.exists("teos/common/.DS_Store"):
    os.remove("teos/common/.DS_Store")

setuptools.setup(
    name="teos_common",
    version="0.0.4",
    author="Sergi Delgado",
    author_email="sergi.delgado.s@gmail.com",
    description="Common library for The Eye of Satoshi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talaia-labs/python-teos",
    packages=['teos.common'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
