import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MatTool", 
    version="1.0.1",
    author="Sachin_S",
    author_email="sachinshanmugam07@gmail.com",
    description="A python package to perform Matrix Operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SACHIN1625/MatTool/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
