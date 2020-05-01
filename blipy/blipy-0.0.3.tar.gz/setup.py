import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blipy",
    version="0.0.3",
    author="Lívia Almeida",
    author_email="leave.ah@gmail.com",
    description="Some BLiP functionalities right out of the box",
    long_description=long_description,
    url="https://github.com/liviaalmeida/blipy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
