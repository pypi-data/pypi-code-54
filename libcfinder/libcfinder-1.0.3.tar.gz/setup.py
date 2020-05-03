import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='libcfinder',
    version='1.0.3',
    scripts=[],
    author='Roberto Pettinau',
    author_email='roberto.pettinau99@gmail.com',
    descrption='Package for finding libc version via offsets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/petitnau/libcfinder',
    packages=setuptools.find_packages(),
      install_requires=[
          'beautifulsoup4', 'requests'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Security"
    ]
)