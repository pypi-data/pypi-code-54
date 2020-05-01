import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pip_grab",
    version="1.0.0.5",
    description="Grabs installed packages in pip every N seconds",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://QuantumNovice.github.io/pip-grab",
    author="QuantumNovice",
    author_email="portabl3lapy@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pip_grab"],
    include_package_data=True,
    install_requires=[],
    #entry_points={"console_scripts": ["pip_grab=pip_grab.__main__:main",]},
    python_requires=">=3.6",
)
