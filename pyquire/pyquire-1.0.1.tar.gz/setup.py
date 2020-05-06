import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("CHANGELOG.md", "r") as fh:
    long_description += fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name="pyquire",
    version="1.0.1",
    author="Vadym Matus",
    author_email="vadym.matus@gmail.com",
    description="Object Oriented API for Quire",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/galava/modules/pyquire",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=required
)
