from setuptools import setup
import setuptools

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="autonis",
    version="1.0.1",
    description="A Python package help you to automate your web easily using python program",
    author="Void",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["urllib3","wikipedia","requests","bs4","speedtest-cli"],
    python_requires='>=3.6',
)
