from setuptools import setup

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

readme = ""
with open("README.rst") as f:
    readme = f.read()

setup(
    name="widgitutils",
    author="Widgit Labs",
    url="https://gitlab.com/widgitlabs/widgitutils",
    project_urls={"Issue tracker": "https://gitlab.com/widgitlabs/widgitutils/issues"},
    version="0.0.9",
    packages=["widgitutils"],
    license="MIT",
    description="A suite of common-use utilities for our cogs.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    tests_require=["black", "flake8", "mypy", "pylint", "pytest"],
    python_requires=">=3.5.3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
