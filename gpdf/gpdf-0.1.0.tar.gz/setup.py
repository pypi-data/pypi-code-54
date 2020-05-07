from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="gpdf",
    version="0.1.0",
    author="Sergey Dyachok",
    author_email="sergey@sdyachok.com.ua",
    description="Gpdf API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyachoksa/gpdf-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
)
