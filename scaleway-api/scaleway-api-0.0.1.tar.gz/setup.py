import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scaleway-api", # Replace with your own username
    version="0.0.1",
    author="Jonathan Baugh",
    author_email="jonathanatx@gmail.com",
    description="An unofficial wrapper around the Scaleway APIs based on Hammock.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanbaugh/scaleway-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "hammock>=0.2.4"
    ]
)