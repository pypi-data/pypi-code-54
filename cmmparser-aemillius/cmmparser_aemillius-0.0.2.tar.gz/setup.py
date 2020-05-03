import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmmparser_aemillius", # Replace with your own username
    version="0.0.2",
    author="Rajender Singh",
    author_email="rajranasingh@rediffmail.com",
    description="parsers for node dump",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aemillius/cmmparser1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)