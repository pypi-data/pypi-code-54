import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "chitrakala",
  version = "0.0.1",
  description = "Annotate images with created at timestamp",
  author = "avellable",
  author_email = "contact@avellable.dev",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = 'https://pypi.org/projects/chitrakala',
  packages = setuptools.find_packages(),
  classifiers= [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ],
  python_requires='>=3.2',
)