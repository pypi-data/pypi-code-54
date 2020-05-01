from setuptools import setup

setup(
    name="falcon-crossorigin",
    version="0.1.2",
    description="Falcon cross-origin middleware",
    url="http://github.com/admiralobviou/falcon-crossorigin",
    author="Alexandre Ferland",
    author_email="aferlandqc@gmail.com",
    license="MIT",
    packages=["falcon_crossorigin"],
    zip_safe=False,
    install_requires=["falcon>=1.4.1"],
    setup_requires=["pytest-runner>=5.2"],
    tests_require=["pytest>=5.4.1"],
    platforms="any",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
