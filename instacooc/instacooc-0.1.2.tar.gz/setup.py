from setuptools import setup

setup(
name='instacooc',
version='0.1.2',
author='Meysam Kheyrollah',
author_email='meysamkheyrollahnejad@gmail.com',
install_requires=[
   'pymysql',
   'pandas'
],
py_modules=["insta_new","storage"],
package_dir={'': "module"},
)
