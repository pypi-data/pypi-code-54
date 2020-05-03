from distutils.core import setup
from setuptools import find_packages

setup(name='chainside-webpos-sdk',
      version='2.0.1',
      packages=find_packages(),
      install_requires=['moveax-sdk-boilerplate==1.1.1'],
      url='https://github.com/chainside/webpos-sdk-python',
      description='Python SDK to integrate ChainsidePay webPOS.'
      )
