from setuptools import setup
from sys import argv

setup(
    name='xlstotex',
    version='0.0.1',
    description='Convert Excel/CSV file to LaTeX table',
    url='https://github.com/tjkessler/xlstotex',
    author='Travis Kessler',
    author_email='travis.j.kessler@gmail.com',
    license='MIT',
    python_requires='~=3.7',
    install_requires=[],
    packages=['xlstotex'],
    entry_points={
        'console_scripts': [
            'xlstotex=xlstotex.cmd:main'
        ]
    },
    zip_safe=False
)
