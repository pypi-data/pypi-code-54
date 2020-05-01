"""Setup script for lasio"""

from setuptools import setup
import os


setup(
    name="lasio",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Read/write well data from Log ASCII Standard (LAS) files",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kinverarity1/lasio",
    author="Kent Inverarity",
    author_email="kinverarity@hotmail.com",
    license="MIT",
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Filesystems",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ),
    keywords="science geophysics io",
    packages=("lasio",),
    install_requires=("numpy",),
    extras_require={"all": ("pandas", "cchardet", "openpyxl", "argparse")},
    tests_require=("pytest>=3.6", "pytest-cov", "coverage", "codecov", "pathlib"),
    entry_points={
        "console_scripts": (
            "las2excel = lasio.excel:main",
            "las2excelbulk = lasio.excel:main_bulk",
            "lasio = lasio:version",
        )
    },
)
