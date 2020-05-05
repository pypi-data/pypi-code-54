from setuptools import setup

setup(name='common_python_programs',
      version='0.1',
      description='This package was created for internal usage',
      url='https://github.com/Saichandarreddy/common_python_programs',
      author='Saichandar Reddy',
      author_email='saichandarreddyt@gmail.com',
      license='MIT',
      packages=['common_python_programs'],
      install_requires=[
            'flask','pandas'
      ],
      zip_safe=False)