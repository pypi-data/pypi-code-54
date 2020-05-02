from setuptools import setup
from glob import glob

data = glob('freetshirts/*.csv')
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='freetshirts',
      version='0.3',
      description='Package to generate email with personalized message to 1500+ colleges.',
      url='http://github.com/iiradia/freetshirts',
      author='Ishaan Radia',
      author_email='iiradia@ncsu.edu',
      license='MIT',
      packages=['freetshirts'],
      install_requires = ['pandas'],
      include_package_data = True,
      package_data = {"freetshirts": 
            data
      },
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False)