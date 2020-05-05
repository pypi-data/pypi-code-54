from setuptools import setup


setup(
    name='roktools',
    version_cc='{version}',
    setup_requires=['setuptools-git-version-cc'],
    author='Rokubun',
    author_email='info@rokubun.cat',
    description='Set of tools used in internal Rokubun projects',
    license='http://opensource.org/licenses/MIT',
    url="https://github.com/rokubun/py-roktools",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    py_modules=['roktools'],
    install_requires=[
        'setuptools >= 8.0',
    ]
)
