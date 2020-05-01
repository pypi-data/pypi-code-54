import setuptools

with open("README.md", "r") as fh:
    README = fh.read()

setuptools.setup(
    name="django-mdeditor-widget", # Replace with your own username
    version="1.1.2",
    author="Timothée Schmoderer",
    author_email="timothee.schmoderer@netcourrier.com",
    description="Django widget to edit markdown in forms",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tschmoderer/django-mdeditor-widget",
    packages=['mdeditor', ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.0",  # Replace "X.Y" as appropriate
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires='>=3.6',
)
