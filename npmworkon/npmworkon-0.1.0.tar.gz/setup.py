from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='npmworkon',
    version='0.1.0',
    author='s0h3ck',
    author_email='s0h3ck@gmail.com',
    description='Node.js virtual environment wrapper on top of nodeenv',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/s0h3ck/npmworkon/',
    py_modules=['npmworkon'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'npmworkon = npmworkon:main'
        ]
    },
    install_requires=[
        'nodeenv',
    ],
    keywords='node npm virtual environment wrapper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
