import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="usbcan",
    version="0.0.4",
    url="https://github.com/laigui/usbcan",
    license='MIT',

    author="Laigui Qin",
    author_email="laigui@gmail.com",

    description="USBCAN driver package",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),
    
    package_data={'': ['ECanVci64.dll']},

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
