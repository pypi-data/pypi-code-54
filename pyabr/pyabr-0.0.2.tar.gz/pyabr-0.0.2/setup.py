import setuptools

with open ("README.md","r") as fh:
	long_description = fh.read()
	
setuptools.setup (
    name="pyabr", # Replace with your own username
    version="0.0.2",
    author="Mani Jamali",
    author_email="manijamali2003@gmail.com",
    description="PyAbr clouding system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manijamali2003/pyabr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
