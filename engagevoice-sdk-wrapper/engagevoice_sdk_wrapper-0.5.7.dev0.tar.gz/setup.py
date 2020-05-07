from setuptools import setup, find_packages
import sys, os

version = '0.5.7'

setup(name='engagevoice_sdk_wrapper',
      version=version,
      description="RingCentral Engage Voice SDK Wrapper for Python",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='RingCentral EngageVoice Engage Contact Center',
      author='Phong Vu',
      author_email='phong.vu@ringcentral.com',
      url='http://engage.ringcentral.com',
      license='',
      packages=find_packages(exclude=[]),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
            'requests'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
