from setuptools import setup, find_packages

requires = [
    'aiofiles',
    'aiodns',
    'tldextract',
    'asyncpg',
    'uvloop',
    'certstream',
    'construct',
    'aiohttp',
    'pyopenssl',
    'b2'
]

setup(name='dnsc',
    version='1.0.0',
    include_package_data=True,
    install_requires=requires,
    packages=find_packages(),
)
