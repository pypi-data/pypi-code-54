import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KmeanBestK", 
    version="0.0.12",
    author="Hilary Feng",
    author_email="fmint88@gmail.com",
    description="An example for k mean algorithm and find the best k",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MintsF/ProgrammingAssignment",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)