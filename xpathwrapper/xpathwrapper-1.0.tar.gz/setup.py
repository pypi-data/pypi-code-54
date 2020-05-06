'''
Created on 09-Oct-2019

@author: elango
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xpathwrapper",
    version="1.0",
    author="Elango SK",
    author_email="elango111000@gmail.com",
    description="Selenium xpath wrapper to easily use in automation python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elaaisolution/FindXpath",
    packages=setuptools.find_packages(),
    keywords = "xpath, selenium, wrapper",
    
)
