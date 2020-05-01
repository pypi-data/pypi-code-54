import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kov_utils",
    version="0.0.1",
    author="Pentek Zsolt",
    author_email="zsoltpentek@yahoo.com",
    description="A small utils package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zselter07/Utilities",
    packages=setuptools.find_packages(),
    install_requires=[
          'fake_useragent'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
