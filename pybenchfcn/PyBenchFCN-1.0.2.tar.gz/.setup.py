import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyBenchFCN", # Replace with your own username
    version="1.0.2",
    author="Yifan He",
    author_email="he.yifan.xs@alumni.tsukuba.ac.jp",
    description="A python implementation of optimization benchmarks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Y1fanHE/PyBenchFCN",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'matplotlib'],
)