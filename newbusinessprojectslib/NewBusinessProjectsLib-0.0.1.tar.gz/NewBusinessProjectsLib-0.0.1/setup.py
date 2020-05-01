from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='NewBusinessProjectsLib',
    version='0.0.1',
    description='Keywords for facile newbusiness project!',
    py_module=["NewBusinessLib"],
    package_dir={'': 'src'},
    long_description="Package which centralized python newbusiness keywords",
    long_description_content_type="text/markdown",
    url="https://github.com/f46io",
    author="Fabio Lima",
    author_email="f46io@icloud.com",
    install_requires=[
        "selenium ~= 3.141.0",
        "robotframework ~= 3.2",
    ],
    Classfiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: MIT",
        "Operating System  ::  OS Independent",
        "Facile.it New Business help out lib "
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
)