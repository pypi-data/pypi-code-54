import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="http-api",
    version="0.2.2",
    author="Syban",
    author_email="author@example.com",
    description="HTTP API for Python using builtin SimpleHTTPServer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
    python_requires='>=3.0',
)