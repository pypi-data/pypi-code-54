#!/usr/bin/python3

import os
import numpy
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize


# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions


extensions = [
    Extension("LSHCy.LSHCy", ["src/LSHCy/LSHlink_Cython.pyx"]),
    Extension(
        "LSHCy.sub.wrong",
        ["src/LSHCy/sub/wrong.pyx", "src/LSHCy/sub/helper.c"]
    ),
]

CYTHONIZE = bool(int(os.getenv("CYTHONIZE", 0)))

if CYTHONIZE:
    compiler_directives = {"language_level": 3, "embedsignature": True}
    extensions = cythonize(extensions, compiler_directives=compiler_directives)
else:
    extensions = no_cythonize(extensions)

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().split("\n")

with open("requirements-dev.txt") as fp:
    dev_requires = fp.read().strip().split("\n")

setup(
    name = "LSHCy",
    version = "1.0",
    description = "Hierarchical Agglomerative Clustering based on Locality Sensitive Hashing",
    author = "Boyang Pan",
    author_email = "boyang.pan@outlook.com",
    requires = ['numpy'],
    url = "https://github.com/Brian1357/STA663-Project-LSHLink",
    ext_modules=extensions,
    install_requires=install_requires,
    include_dirs = [numpy.get_include(), "LSHlinkCython/"],
    extras_require={
        "dev": dev_requires,
        "docs": ["sphinx", "sphinx-rtd-theme"]
    },
)
