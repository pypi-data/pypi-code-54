import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as requirement_file:
   require_dependencies = requirement_file.read().splitlines()

setuptools.setup(
    name="django-cloud-logging",
    version="0.1.0",
    author="Django Circle",
    author_email="djangocircle@gmail.com",
    description="A package which stores your django application logs in google stackdriver.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=require_dependencies,
    python_requires='>=3',
)