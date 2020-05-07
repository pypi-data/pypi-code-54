import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="web-downloader", # Replace with your own username
    version="0.0.4",
    author="Gabriel Chung",
    author_email="gabrielchung1128@gmail.com",
    description="A Python package using Selenium to download web content",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/gabrielchung/WebDownloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)