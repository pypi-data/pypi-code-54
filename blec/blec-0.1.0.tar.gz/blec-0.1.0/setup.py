import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blec",
    version="0.1.0",
    author="igrmk",
    author_email="igrmkx@gmail.com",
    description="Alpha blending calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igrmk/blec",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    scripts=['bin/blec'],
)
