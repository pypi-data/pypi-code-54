import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eegbase-nix-converter",
    version="1.0.0",
    author="Jan Sedivy",
    author_email="honza.seeda@gmail.com",
    description="EEGbase -> NIX converter converts BranVision/odML dataset to a NIX container file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/honza.seda/eegbase-nix-converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True
)
