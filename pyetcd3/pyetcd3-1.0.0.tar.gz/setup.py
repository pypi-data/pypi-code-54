import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()


setuptools.setup(
    name = "pyetcd3",
    version = "1.0.0",
    author = "Alias",
    author_email = "aliasmic@live.cn",
    description = "Python etcd v3 client library",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/caslt/pyetcd3",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires = '>=3.6'

)