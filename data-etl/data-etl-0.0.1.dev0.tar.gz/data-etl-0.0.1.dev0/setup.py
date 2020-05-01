import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-etl", # Replace with your own username
    version="0.0.1dev",
    author="GigiSR",
    url="https://github.com/gigisr/data_etl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
