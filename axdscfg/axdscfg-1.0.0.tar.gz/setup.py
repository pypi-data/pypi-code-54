
import setuptools
import axdscfg

requirements = ["configparser>=3.7.4",
                "PyNaCl==1.3.0"] 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=axdscfg.__title__,
    version=axdscfg.__version__,
    author=axdscfg.__author__,
    author_email=axdscfg.__email__,
    description=axdscfg.__summary__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'axdscfg = axdscfg:main'
        ]
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
    python_requires='>=3.5',
)