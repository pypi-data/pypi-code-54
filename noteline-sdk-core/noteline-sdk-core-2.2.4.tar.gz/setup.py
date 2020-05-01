import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noteline-sdk-core",
    version="2.2.4",
    author="Viacheslav Kovalevskyi",
    author_email="viacheslav@kovalevskyi.com",
    description="core Noteline SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noteline-org/noteline-core",
    packages=setuptools.find_namespace_packages(include=["noteline.*"]),
    install_requires=[
        "nbformat",
        "smart_open"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
