from setuptools import setup

setup(
    name='short-urls-client',
    version='1.0.0',
    description='A python client for the https://github.com/jamesridgway/aws-lambda-short-url project.',
    long_description=open('README.md').read(),
    author='James Ridgway',
    url='https://github.com/jamesridgway/short-urls-client',
    license='MIT',
    packages=['short_urls'],
    scripts=['bin/short-urls'],
    install_requires=["pyperclip", "requests"]
)