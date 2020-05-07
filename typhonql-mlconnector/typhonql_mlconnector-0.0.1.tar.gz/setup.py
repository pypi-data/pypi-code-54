import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typhonql_mlconnector",
    version="0.0.1",
    author="PAPAIOANNOU GEORGE",
    author_email="papageorge94@gmail.com",
    description="typhonql-mlconnector package for queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ge0rge.pap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
