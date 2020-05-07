import setuptools
import teos10

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="teos10",
    version=teos10.__version__,
    author=teos10.__author__,
    author_email="m.p.humphreys@icloud.com",
    description="Unofficial Python implementation of the TEOS-10 properties of water",
    url="https://github.com/mvdh7/teos10",
    packages=setuptools.find_packages(),
    install_requires=["autograd==1.3"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
)
