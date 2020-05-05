import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="freehand",
    version="0.0",
    author="Mitchell James Wagner",
    author_email="mitchell.j.wagner@gmail.com",
    description="A Python 3 graphing library designed to produce rasterized emulations of freehand drawing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mitchwagner/freehand",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ]
)
