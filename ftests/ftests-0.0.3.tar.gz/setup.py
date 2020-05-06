import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='ftests',
    version='0.0.3',
    author='Hugo Atomot',
    author_email='hugoatomot@gmail.com',
    description='A simple and efficient functional testing tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Atomot/ftests',
    packages=setuptools.find_packages(),
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
    ],
    python_requires='>=3.7',
    project_urls={
        'Source': 'https://github.com/Atomot/ftests',
    },
    entry_points={
        'console_scripts': [
            'ftests = ftests.__main__:main'
        ]
    },
)
