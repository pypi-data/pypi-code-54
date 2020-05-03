import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zoek",
    version="0.0.1",
    author="Davey Kreeft, Tein de Vries",
    author_email="dkreeft@xccelerated.io, teindevries@gmail.com",
    description="Search for files and directories in your terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dkreeft/zoek",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
