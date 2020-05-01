from setuptools import setup

with open("README.md", "r") as fh:
      long_description = fh.read()

setup(name='portela',
      version='0.0.3',
      description='a simple port allocator',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/perfecto25/portela',
      author='mreider',
      author_email='mike.reider@gmail.com',
      license='MIT',
      packages=['portela'],
      keywords='portela port listener web server',
      zip_safe=True,
      scripts=['bin/portela'],
      entry_points={'console_scripts': ['portela=portela.__main__:entry']}
      )