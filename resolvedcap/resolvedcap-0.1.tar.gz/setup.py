import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="resolvedcap",
    version="0.1",
    author="Korud",
    author_email="khorud@yahoo.com",
    description="2Captcha Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khorud",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    # include_package_data=True,
    install_requires= ['selenium'],
    python_requires= '>=3',
)