import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='vim_unitex',
    version='0.0.1',
    author='Dow Drake',
    author_email='dowdrake@msn.com',
    description='Replace Latex snippets with unicode',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://bitbucket.com/ddrake999/vim_unitex',
    license='MIT',
    scripts=['scripts/tex2unicode'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
