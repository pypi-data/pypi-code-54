"""

"""
import setuptools


"""setup"""
with open('./README.md', 'r') as fh:
    long_description = fh.read()

version = "0.0.1dev2"

setuptools.setup(
    name='allennlp-utils',
    version=version,
    author='wj-Mcat（吴京京）',
    author_email='1435130236@qq.com',
    description='allennlp practical code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    url='https://github.com/wj-Mcat/allennlp-utils',
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
