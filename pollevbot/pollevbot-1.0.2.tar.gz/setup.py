from setuptools import setup, find_packages

# Source: https://github.com/pypa/sampleproject/blob/master/setup.py

setup(
    name='pollevbot',
    version='1.0.2',
    description='A Python script that automatically responds to polls on PollEverywhere.',
    url='https://github.com/danielqiang/pollevbot',
    author='Daniel Qiang',
    author_email='daniel_qiang@hotmail.com',
    install_requires=['requests', 'bs4'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.7',
    packages=find_packages(),
    include_package_data=True
)
