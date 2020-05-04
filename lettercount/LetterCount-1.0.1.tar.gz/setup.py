import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LetterCount", 
    version="1.0.1",
    author="Sachin_S",
    author_email="sachinshanmugam07@gmail.com",
    description="A small package to count repetition of a letter in a string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SACHIN1625/LetterCount/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
