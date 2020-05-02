from setuptools import setup, find_packages

with open('README.md') as f:
    d = f.read()
setup(
    long_description = d,
    name='Tello modules',
    version='0.1dev',
    packages=find_packages(),
    install_requires=['pyserial']
)
