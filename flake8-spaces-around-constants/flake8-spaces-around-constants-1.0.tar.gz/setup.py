from __future__ import with_statement
from setuptools import setup


def get_version(fname='flake8_spaces_around_constants.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.md',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)

install_requires = ['flake8']

setup(
    name='flake8-spaces-around-constants',
    version=get_version(),
    description='Check whether your constant values have leading or trailing spaces',
    long_description=get_long_description(),
    keywords='flake8 constants leading trailing space',
    author='Unleashed NV',
    author_email='development@unleashed.be',
    url='https://github.com/vikingco/flake8-spaces-around-constants',
    license='MIT',
    py_modules=['flake8_spaces_around_constants'],
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'flake8_spaces_around_constants = flake8_spaces_around_constants:ConstantSpacesChecker',
        ],
    },
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
