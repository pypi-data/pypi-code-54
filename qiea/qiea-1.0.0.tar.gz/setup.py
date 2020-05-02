from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="qiea",
    version="1.0.0",
    description="A Python package for Quantum Inspired Evolutionary Algorithms.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/adhishagc/qiea",
    author="Adhisha Gammanpila",
    author_email="adhishagc@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["framework"],
    include_package_data=True,
    install_requires=["qiskit","tsplib95","networkx"],
    entry_points={
        "console_scripts": [
            
        ]
    },
)