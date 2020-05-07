from setuptools import setup
import codecs

__version__ = "0.0.0"
URL = "https://github.com/daculous/daculous-py"

setup(
    name="daculous",
    version=__version__,
    description="Python library for DACulous",
    long_description="",
    download_url="{}/tarball/{}".format(URL, __version__),
    author="DACulous developers",
    author_email="info@daculous.org",
    maintainer="DACulous developers",
    maintainer_email="info@daculous.org",
    url=URL,
    keywords=[],
    packages=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    include_package_data=True,
)
