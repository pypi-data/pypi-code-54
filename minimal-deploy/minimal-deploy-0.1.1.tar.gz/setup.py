from setuptools import setup

setup(
    name="minimal-deploy",
    description='A minimal Python package',
    author='Talley',
    author_email='talley.lambert@gmail.com',
    url='https://github.com/tlambert03/minimal-deploy',
    packages=['minimal'],
    use_scm_version={"write_to": "minimal/_version.py"},
    setup_requires=['setuptools_scm'],
)