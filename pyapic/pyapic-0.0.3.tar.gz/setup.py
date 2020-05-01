import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyapic",
    version="0.0.3",
    author="Jesús Moreno Amor",
    author_email="jesus@morenoamor.com",
  	description='API Connect 2018 Management API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jmorenoamor/pyapic',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'oyaml',
        'requests',
        'python-dateutil'
    ],
    python_requires='>=3.6',
)
