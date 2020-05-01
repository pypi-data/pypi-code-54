from os import *
def install(s):
    system('python -m pip install '+s+'>pip_install.log')
def uninstall(s):
    system('python -m pip unstall '+s+'>pip_install.log')
def upgrade(s):
    system('python -m pip --upgrade '+s+'>pip_install.log')
