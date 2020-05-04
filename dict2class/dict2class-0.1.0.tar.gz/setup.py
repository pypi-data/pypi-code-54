import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='dict2class',
    version='0.1.0',
    author='Brennen Herbruck',
    author_email='brennen.herbruck@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pypa/sampleproject',
    packages=['dict2class'],
    python_requires='>=3.6',
)