from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name             = "isodaterange",
    version          = "1.0.1",
    author           = "Tim Barnes",
    author_email     = "tdba@bas.ac.uk",
    description      = "Python module to convert an ISO date/time into a range",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url              = "https://github.com/antarctica/isodaterange",
    license          = "Open Government License v3.0",
    packages         = ["isodaterange"],
    install_requires = [
        "isodate"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3"
    ]
)
