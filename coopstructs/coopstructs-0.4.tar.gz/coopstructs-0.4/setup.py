from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='coopstructs',
      version='0.4',
      description='basic commonly used data structures for python applications',
      url='https://github.com/tylertjburns/datastructs',
      author='tburns',
      author_email='tyler.tj.burns@gmail.com',
      license='MIT',
      long_description=long_description,
      zip_safe=False)