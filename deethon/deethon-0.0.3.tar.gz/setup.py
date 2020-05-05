import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deethon",
    version="0.0.3",
    author="Aykut Yilmaz",
    author_email="aykuxt@gmail.com",
    description="Python 3 library to easily download music from Deezer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aykuxt/deethon",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'mutagen',
        'requests',
        'Crypto'
    ],
    python_requires='>=3.6',
)