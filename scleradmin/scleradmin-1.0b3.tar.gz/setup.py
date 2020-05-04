import setuptools

with open("README.md", "rt") as f:
    long_description = f.read()

setuptools.setup(
    name="scleradmin",
    version="1.0-beta-3",
    author="Sclera, Inc.",
    author_email="dev@scleradb.com",
    description="Sclera Platform Administration Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scleradb/scleradmin",
    keywords="scleradb sclera virtualization admin installer",
    packages=["src"],
    package_data={
        "src": ["config/sclera.conf"],
    },
    install_requires=['requests'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Java",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Installation/Setup"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "scleradmin = src:main",
        ],
    },
)
