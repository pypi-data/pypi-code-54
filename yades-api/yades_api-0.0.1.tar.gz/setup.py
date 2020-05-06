from os import path
from setuptools import setup

from yades_api import __version__, __author__, __email__


root_dir = path.abspath(path.dirname(__file__))

with open(path.join(root_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='yades_api',
    version=__version__,
    author=__author__,
    author_email=__email__,
    packages=['yades_api'],
    include_package_data=True,
    url='https://github.com/yades/yades-api/',
    license='MIT',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='aiohttp asyncio',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'yades_api=yades_api.__main__:main',
        ],
    },
)
