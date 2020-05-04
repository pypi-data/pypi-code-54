import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AnsiPrint",
    version="0.0.6",
    author="ChezCoder",
    author_email="mrpizzaguyytb@gmail.com",
    description="Lightweight package for colored text in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://repl.it/@ChezCoder/AnsiPrint",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)