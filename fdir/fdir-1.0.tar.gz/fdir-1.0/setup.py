from setuptools import setup, Extension
from setuptools.command.install import install
import subprocess
import os

with open("README.md", "r") as md:
    doc = md.read()

class PackageInstaller(install):
    def runInstall(self):
        command = "git clone https://github.com/m-zayan/fdir.git"
        process = subprocess.Popen(command, shell=True, cwd="fdir")
        process.wait()
        install.runInstall(self)
        
module = Extension('fdir',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0.1')],
                    sources = ['src/_fdir_.c'])



setup(
    name="fdir",
    version="1.0",
    description = 'Module For Iterating through OS Directories',
    url="https://github.com/m-zayan/fdir",
    author = 'Mohamed Zayan',
    author_email="zayanm410@gmail.com",
    license ='MIT',
    keywords = ['Files', 'Directories', 'OS'],  
    classifiers=[
    'Development Status :: 3 - Alpha',            
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
    long_description=doc,
    long_description_content_type="text/markdown",
    cmdclass={'install': PackageInstaller},
    include_package_data=True,
    ext_modules = [module]
)

