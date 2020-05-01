from setuptools import setup, find_packages  

setup(  
    name='start-cli',
    version='0.0.1',
    description='scaffold for quick start project',
    author='codingcat',
    author_email='istommao@gmail.com',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/istommao/start-cli',
    keywords='scaffold',
    entry_points="""
    [console_scripts]
    start-cli=src.main:run
    """,
)
