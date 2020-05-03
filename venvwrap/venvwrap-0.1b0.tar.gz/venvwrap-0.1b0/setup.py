import setuptools

with open("README.md", 'r') as fh:
    readme = fh.read()

setuptools.setup(
        name="venvwrap",
        version="0.1b0",
        author="hunkeydee",
        author_email="unknown@unk.invalid",
        description="A collection of bash functions for venv management",
        long_description=readme,
        long_description_content_type="text/markdown",
        url="https://github.com/hunkeydee/venvwrap",
        packages=None,
        scripts=['venvwrap.sh'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Environment :: Console"
            ],
        platforms="Debian GNU/Linux 10 (buster)",
        python_requires=">=3.6",
        )
