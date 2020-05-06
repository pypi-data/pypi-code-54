import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-BRN", 
    version="0.0.1",
    author="Josine Bruin",
    author_email="josine.bruin@cqm.nl",
    description="An example package",
    long_description="Generates all BE options for a given BE size, max pallet weight, max pallet height and max BE weight.",
    long_description_content_type="text/markdown",
    url="https://github.com/josine-cqm/BEgenerator",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)