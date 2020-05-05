import os
from setuptools import setup, find_packages

BASEDIR = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(BASEDIR, 'VERSION')).read().strip()

# Dependencies (format is 'PYPI_PACKAGE_NAME[>=]=VERSION_NUMBER')
BASE_DEPENDENCIES = [
    'numpy>=1.18',
    'tqdm>=4.46'
]

# TEST_DEPENDENCIES = [
# ]
#
# LOCAL_DEPENDENCIES = [
# ]

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(BASEDIR))

setup(
    name='simple-neural-net',
    packages=find_packages(),
    version=VERSION,
    include_package_data=True,
    description='Minimal framework for creating a simple neural net',
    long_description=open('README.md').read(),
    url='https://github.com/tcquinn/simple-neural-net',
    author='Theodore Quinn',
    author_email='tcquinn@tcquinn.org',
    install_requires=BASE_DEPENDENCIES,
    # tests_require=TEST_DEPENDENCIES,
    # extras_require = {
    #     'test': TEST_DEPENDENCIES,
    #     'local': LOCAL_DEPENDENCIES
    # },
    keywords=['neural network', 'deep learning'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
