import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="talmud_debts",
    version="0.1.2",
    author="Data Dolitle",
    author_email="datadolittle@gmail.com",
    description="Split estate to array of creditors using talmudic game theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Datadolittle/Talmud_Debts",
    packages=['talmud_debts'],
    install_requires=['markdown'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
