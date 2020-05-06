import setuptools
import setuptools_autover
from distutils.core import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name='inspy-logger',
    version='1.0.3',
    packages=['inspy_logger'],
    url='https://github.com/Inspyre-Softworks/inspy_logger',
    license='WTFYW',
    author='Taylor-Jayde B. Blackstone',
    author_email='t.blackstone@inspyre.tech',
    description='A module that gives you a formatted logger that is also far more informative than the default logger',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='logger color formatted easy inspyre debug',
    install_requires=[
        'colorlog'
    ]

)
