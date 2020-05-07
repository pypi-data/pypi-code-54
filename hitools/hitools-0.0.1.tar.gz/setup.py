from setuptools import find_packages, setup


with open("README.md", 'r') as readme:
    long_description = readme.read()

setup(
    author='HiLearn',
    author_email='info@hilearn.io',
    license='MIT',
    test_suite='nose.collector',
    tests_require=['nose'],
    packages=find_packages(exclude=['test', 'test.*']),
    name='hitools',
    version='0.0.1',
    description='Package of utility functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
)

