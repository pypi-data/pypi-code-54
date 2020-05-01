import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sym-types",
    version="0.0.10",
    author="Sym Inc",
    author_email="info@symops.io",
    description="Generated protobufs for Sym types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/symopsio/types",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.6',
)
