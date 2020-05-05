import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rfile",  # Replace with your own username
    version="0.2.0",
    author="Scott Walsh",
    author_email="scott@invisiblethreat.ca",
    description="A package to make R installed packages somewhat portable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/invisiblethreat/rfile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['scripts/rfile'],
    python_requires='>=3.6',
)
