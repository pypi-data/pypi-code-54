import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="readpass",
    version="0.0.2",
    author="ChezCoder",
    author_email="mrpizzaguyytb@gmail.com",
    description="function to modify user input",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="https://repl.it/@ChezCoder/readpass",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)