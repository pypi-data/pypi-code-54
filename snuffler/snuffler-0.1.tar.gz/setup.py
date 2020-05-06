import setuptools

with open('README.md', 'r')as fh:
    long_description = fh.read()

setuptools.setup(
        name='snuffler',
        version='0.1',
        description='Sniffing Tools',
        url='https://github.com/m1ghtfr3e/snuffler',
        author='m1ghtfr3e',
        packages=setuptools.find_packages(),
        zip_safe=False,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            ],
        ) 
