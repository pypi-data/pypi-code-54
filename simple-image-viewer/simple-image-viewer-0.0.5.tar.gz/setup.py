import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-image-viewer", 
    version="0.0.5",
    author="Saeid Hosseinipoor",
    author_email="shossei1@stevens.edu",
    description="A simple image viewer for computer vision purposes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saeid-h/Simple-Image-Viewer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)