from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name = "pysample55321",
    version = "1.0.3",
    description = "A sample python package with cpp",
    long_description = "README.md",
    classifiers = ["Development Status :: 1 - Planning", "Environment :: Console", "Intended Audience :: Developers", "License :: OSI Approved :: MIT License", "Operating System :: POSIX", "Programming Language :: Python :: 3.7"],
    keywords = "sample hello test",
    url = "http://github.com/horia141/tabletest",
    author = "Mansoor Nasir",
    author_email = "cheema@fortiss.org",
    license = "MIT",
    packages=["pysample55321"],
    install_requires=[],
    test_suite = "nose.collector",
    tests_require=["nose"],
    zip_safe=False,
)

