from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

name = "chombopy"
version = "0.2"
release = "0.2.1"

test_requires = ["pytest-cov", "coverage", "pytest-html"]
setup_requires = ["wheel", "sphinx", "recommonmark>=0.5.0", "numpydoc", "black"]

setup(
    name=name,
    version=release,
    description="Running, analysing and plotting Chombo simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrgparkinson/chombopy",
    author="Jamie Parkinson",
    author_email="jamie.parkinson@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=setup_requires,
    python_requires=">=3.6",
    install_requires=[
        "matplotlib>=3.0.0",
        "Shapely>=1.6.0",
        "geopandas>=0.6.2",
        "scipy>=1.2.0",
        "scikit-image>=0.16.2",
        "xarray>=0.11.3",
        "h5py>=2.9.0",
        "numpy>=1.16.0",
        "descartes",
    ]
    + test_requires
    + setup_requires,
    tests_require=test_requires,
    zip_safe=False,
)
