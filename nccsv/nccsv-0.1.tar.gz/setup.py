# setup.py
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="nccsv",
    version="v0.1",
    description="Ncurses CSV Editor written in Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ssebs/nccsv",
    author="Sebastian Safari",
    author_email="contact@ssebs.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6.0",
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "nccsv = nccsv.__main__:main",
        ],
        "gui_scripts": [
            "nccsv = nccsv.__main__:main",
        ]
    }
)
