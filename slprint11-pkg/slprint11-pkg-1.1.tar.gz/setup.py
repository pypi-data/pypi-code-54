import setuptools


with open("README.rst", "r") as fh1:
    long_description = fh1.read()
	
setuptools.setup(
    name="slprint11-pkg",
    version="1.1",
    author="Ronaldo Augusto Vasques de Souza",
    author_email="vasquessouza.75@gmail.com",
    description="Simple module to display a text with a time interval between each characters.",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/RonaldoVasques/slowprint",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",        
		"Environment :: Console",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Operating System :: Microsoft :: Windows :: Windows 10",
		"Operating System :: MacOS",
		"Operating System :: POSIX",
		"Topic :: Terminals",
		"Topic :: System :: Shells",
		"Topic :: Software Development :: Libraries",
		"Topic :: Desktop Environment"		
    ],
    python_requires='>=3.0',
)