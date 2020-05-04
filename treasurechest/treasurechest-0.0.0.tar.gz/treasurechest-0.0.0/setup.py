from setuptools import setup, find_packages

setup(name='treasurechest',
      version='0.0.0',
      description='',
      author='Kevin Froman',
      author_email='beardog@mailbox.org',
      url='',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=['PyNacl'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
      ],
     )
