import os
from setuptools import setup, find_packages


dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="truckman",
    version="0.0.1",
    description="Save and load Docker named volumes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tsuribori",
    author_email="tsuribori@tutanota.com",
    url="https://github.com/Tsuribori/truckman",
    keywords="docker volume save load backup transfer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5",
    install_requires=['docker'],
    entry_points={
      'console_scripts': [
          'truckman=truckman:main'
      ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving"
    ]
)
