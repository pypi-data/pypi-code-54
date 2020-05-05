import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tali",
    version="0.0",
    author="Mitchell James Wagner",
    author_email="mitchell.j.wagner@gmail.com",
    description="Tali: a hashmap-y Lisp.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tali-software-foundation/tali-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ]
)
