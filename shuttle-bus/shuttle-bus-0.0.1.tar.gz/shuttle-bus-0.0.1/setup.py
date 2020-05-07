import setuptools

try:
    with open("README.md", "r") as fh:
        LONG_DESC = fh.read()
except:
    LONG_DESC = ""

setuptools.setup(
    name="shuttle-bus",
    version="0.0.1",
    author="Jason Watson",
    author_email="jbw@jbw.cc",
    description="",
    url="https://github.com/jbw/shuttle-bus",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    packages=["shuttle-bus"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)