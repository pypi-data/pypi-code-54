import setuptools
from setuptools.command.sdist import sdist

with open("README.md", "r") as fh:
    long_description = fh.read()


class Sdist(sdist):

    def run(self):
        self.run_command('compile_catalog')
        sdist.run(self)


setuptools.setup(
    name="osirisvalidator",
    version="0.1.0",
    author="David Veiga",
    author_email="david@david.blog.br",
    description="Validators for fields in Flask-Restless",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidaug/osiris",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)
