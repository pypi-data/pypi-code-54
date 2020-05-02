from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


with open('requirements-test.txt') as f:
    test_requirements = f.read().splitlines()


setup(
    name='pyavro',
    author='Mitchell Lisle',
    author_email='m.lisle90@gmail.com',
    description="A Python Avro Schema Builder",
    install_requires=requirements,
    packages=find_packages(),
    setup_requires=[],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mitchelllisle/pyavro',
    version='0.4.0',
    zip_safe=False,
)
