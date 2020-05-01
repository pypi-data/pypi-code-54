from setuptools import setup, find_packages
with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    # Metadata
    name = 'SDDetector',
    version = '0.1.0',
    description = 'lightweight video detection',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/thomascong121/SocialDistance',
    author = 'SocialDistance model contributors',
    author_email = 'thomascong@outlook.com',
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)