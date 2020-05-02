import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='aMath',
    version='1.1',
    license="AJL",
    description="A small Math basic Ops package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Arun',
    author_email='arrrsh@gmail.com',
    url="https://www.deexams.com/",
    packages=setuptools.find_packages(), #['aMath'],  # same as name
    install_requires=[],  # external packages as dependencies
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
