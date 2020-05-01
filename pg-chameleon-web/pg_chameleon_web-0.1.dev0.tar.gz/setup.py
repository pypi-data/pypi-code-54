#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, setuptools

def readme():
	with open('README.rst') as f:
		return f.read()

package_data = {'pg_cham_web': ['LICENSE.txt']}

setup(
	name="pg_chameleon_web",
	version="0.1DEV",
	description="Web interface for pg_chameleon",
	long_description=readme(),
	author = "Federico Campoli",
	author_email = "the4thdoctor.gallifrey@gmail.com",
	maintainer = "Federico Campoli", 
	maintainer_email = "the4thdoctor.gallifrey@gmail.com",
	url="https://gitlab.com/the4thdoctor/pg_chameleon_web",
	license="BSD License",
	platforms=[
		"linux"
	],
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"Intended Audience :: Information Technology",
		"Intended Audience :: System Administrators",
		"Natural Language :: English",
		"Operating System :: POSIX :: BSD",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Topic :: Database :: Database Engines/Servers",
		"Topic :: Other/Nonlisted Topic"
	],
	py_modules=[
		"pg_cham_web.__init__",
	],
	scripts=[
		"pgcw.py",
		"pgcw",
	],
	install_requires=[
		'psycopg2-binary>=2.8.3', 
		'PyYAML>=5.1.2', 
		'Flask>=1.1.2', 
		'pg_chameleon>=2.0', 
	],
	include_package_data = True, 
	package_data=package_data,
	packages=setuptools.find_packages(),
	python_requires='>=3.6',
	keywords='postgresql replica migration flask web',
	
)
