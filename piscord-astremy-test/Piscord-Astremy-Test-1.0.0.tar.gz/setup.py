import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Piscord-Astremy-Test", # Replace with your own username
    version="1.0.0",
    author="Astremy",
    author_email="",
    description="Piscord is a python framework to communicate with the Discord api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Astremy/Piscord",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)