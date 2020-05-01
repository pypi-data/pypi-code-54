import setuptools

try:
    with open("README.md", "r") as fh:
        LONG_DESC = fh.read()
except:
    LONG_DESC = ""

setuptools.setup(
    name="singleton_pattern_decorator",
    version="1.0.5",
    author="Jason Watson",
    author_email="jbw@jbw.cc",
    description="Singleton decorator",
    url="https://github.com/jbw/singleton-pattern-decorator",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    packages=["singleton_pattern_decorator"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
