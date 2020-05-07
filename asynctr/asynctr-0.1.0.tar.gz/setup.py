import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asynctr", # Replace with your own username
    version="0.1.0",
    author="EraseKesu",
    author_email="eitan.olchik@gmail.com",
    description="An Asynchronous Google Translate Easy to use API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EraseKesu/asynctr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
