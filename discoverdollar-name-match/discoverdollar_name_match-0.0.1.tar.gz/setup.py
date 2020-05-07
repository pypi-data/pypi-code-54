from setuptools import setup

setup(
    name='discoverdollar_name_match',
    version='0.0.1',
    description='My private package from private github repo',
    url='https://github.com/discoverdollartech/discoverdollar_name_match',
    author='srikant hiremath',
    author_email='srikant.hiremath@discoverdollar.com',
    license='MIT',
    packages=['discoverdollar_name_match'],
    install_requires=['pandas>=0.24.2','fuzzywuzzy>=0.18.0','cleanco','numpy>=1.16.2'],
    zip_safe=False
)
