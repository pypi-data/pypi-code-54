import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shared_image_processing",
    version="0.0.2",
    author="Matt-Conrad",
    author_email="mattgrayconrad@gmail.com",
    description="Image processing library for sharing across projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Matt-Conrad/SharedImageProcessing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)