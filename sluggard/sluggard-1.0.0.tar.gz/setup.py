from setuptools import setup


package_name = 'sluggard'


with open('README.rst') as fp:
    long_description = fp.read()


setup(
    name=package_name,
    packages=[package_name],
    version='1.0.0',
    author='SiLeader and Cerussite',
    description='directory packaging tool',
    keywords='packaging, compression, archiving',
    long_description=long_description,
    url='https://github.com/SiLeader/sluggard',

    entry_points={
        'console_scripts': [
            'sluggard = sluggard.sluggard:main'
        ],
    },

    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: System :: Archiving :: Packaging',
    ],
)
