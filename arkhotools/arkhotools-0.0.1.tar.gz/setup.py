import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arkhotools", # Replace with your own username
    version="0.0.1",
    author="Marcelo Silva",
    author_email="msilva@arkho.tech",
    description="Set de herramientas para desarrollo en lamdba python AWS",
    url=" https://gitlab.com/arkhotech/arkholabs/lambda-tools.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
