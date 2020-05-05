import setuptools
import shutil
import os
import glob


CLEAN_FILES = './build ./dist ./*.egg-info'.split(' ')

for path_spec in CLEAN_FILES:
    # Make paths absolute and relative to this path
    abs_paths = glob.glob(os.path.normpath(path_spec))
    for path in [str(p) for p in abs_paths]:
        print('removing', os.path.relpath(path))
        shutil.rmtree(path)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deethon",
    version="0.0.5",
    author="Aykut Yilmaz",
    author_email="aykuxt@gmail.com",
    description="Python3 library to easily download music from Deezer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aykuxt/deethon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["mutagen", "requests", "Crypto"],
    python_requires=">=3.6",
)
