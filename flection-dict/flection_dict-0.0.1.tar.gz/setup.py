import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flection_dict",
    version="0.0.1",
    author="Michał Szczepaniak",
    author_email="michal.szczepaniak1999@gmail.com",
    description="Library allows quick and convenient flection finding.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twistzzmc/Dictionary",
    packages=setuptools.find_packages(),
    install_requires=['marisa_trie'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)