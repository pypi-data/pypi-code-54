from setuptools import find_packages,setup

setup(
name="twittercooc",
version="1.0.0",
author="Meysam Kheyrollah",
author_email="meysamkheyrollahnejad@gmail.com",
install_requires=[
   'pymysql',
   'pandas',
   'json',
   'requests'
],
py_modules=["twitter_new","storagetwitter"],
package_dir={'': "module"},

)
