import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-mdeditor-widget", # Replace with your own username
    version="1.1.0",
    author="Timothée Schmoderer",
    author_email="timothee.schmoderer@netcourrier.com",
    description="Django widget to edit markdown in forms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tschmoderer/django-mdeditor-widget",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
