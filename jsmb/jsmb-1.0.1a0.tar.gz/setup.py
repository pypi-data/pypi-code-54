import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsmb",  # Replace with your own username
    version="1.0.1a",
    author="Jonatan dos Santos da Silva",
    author_email="xjhonn@gmail.com",
    description="Paquete de ayuda para usar SAMBA con Python con smb.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
