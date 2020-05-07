from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wakalinus',
    packages=['wakalinus'],
    install_requires=['janome'],

    version='0.1.0',
    license='MIT',

    author='Tatsuya Abe',
    author_email='abe12@mccc.jp',

    url='https://github.com/AjxLab/wakalinus',

    desription='A simple sentiment analysis utility for Japanese.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='setiment nlp japanese',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
