from setuptools import setup

with open("dsnd_probability_cbarr/README.md", "r") as fh:
    long_description = fh.read()

setup(name='dsnd_probability_cbarr',
      version='1.1',
      description='Gaussian and Binomial distributions',
      long_description = long_description,
      long_description_content_type="text/markdown",
      packages=['dsnd_probability_cbarr'],
      author = 'Cindy Barrientos',
      author_email = 'cbarrien@ucsd.edu',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)
