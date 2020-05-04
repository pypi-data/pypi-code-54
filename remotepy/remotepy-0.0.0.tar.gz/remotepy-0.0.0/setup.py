import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remotepy",
    version="0.0.0",
    author="Farukh Dilawar Tamboli",
    author_email="farukht@gmail.com",
    description="remote Py allows Python functions to be called remotely from multiple languages including JavaScript, CSharp and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.remotePy.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)