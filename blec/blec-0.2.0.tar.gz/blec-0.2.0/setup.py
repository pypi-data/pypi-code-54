import os
import codecs
import setuptools

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version():
    for line in read('bin/blec').splitlines():
        if line.startswith('__version__'):
            return line.split("'")[1]
    return ''


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='blec',
    version=get_version(),
    author='igrmk',
    author_email='igrmkx@gmail.com',
    description='Alpha blending calculator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/igrmk/blec',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
    scripts=['bin/blec'],
)
