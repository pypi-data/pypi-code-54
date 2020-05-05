

from setuptools import setup, find_packages

version_namespace = {}
with open('qconf/version.py') as f:
    exec(f.read(), version_namespace)

test_deps = ['pytest']

setup(name='qconf',
      version=version_namespace['__version__'],
      description='Quick Parser and Config',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Intended Audience :: Developers',
      ],
      url='https://github.com/vossenv/qconf',
      maintainer='Danimae Vossen',
      maintainer_email='vossen.dm@gmail.com',
      packages=find_packages(),
      install_requires=[
          'PyYAML',
          'python_dateutil',
      ],
      extras_require={
          'test': test_deps,
      },
      tests_require=test_deps,
      )
