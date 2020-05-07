import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="custom_math_operations_gangulis",
    version="0.0.2",
    author="Subhajit Ganguli",
    author_email="subhajit.ganguli-non-empl@moodys.com",
    description="Some useful mathematical operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.moodys.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)