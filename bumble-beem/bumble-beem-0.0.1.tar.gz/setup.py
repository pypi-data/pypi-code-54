from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.1'

requires = [
    'Click'
]
dev_requires = {
    "dev": [
        "pytest"
    ]
}

entry_points = """
    [console_scripts]
    wasp=cli.cli:cli
"""

setup(
    name='bumble-beem',
    version=VERSION,
    author='DistortedLogic/Memehub',
    author_email='jermeek@gmail.com',
    url='http://pypi.python.org/pypi/bumble-beem/',
    license='LICENSE.txt',
    description='A lightweight python library for interacting with the Hive Blockchain',
    long_description=long_description,
    packages=find_namespace_packages(where='src', exclude=['docs', 'tests*']),
    install_requires=requires,
    extras_require=dev_requires,
    package_dir={'': 'src'},
    keywords=['hive', 'steem', 'library', 'api', 'rpc'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
    entry_points=entry_points,
    include_package_data=True
)
