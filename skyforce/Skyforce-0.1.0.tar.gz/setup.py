#
# MIT License
#
# Copyright (c) 2017 - 2020 Firebolt Inc,
# Copyright (c) 2020 - Present Aaron Ma.
# All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from setuptools import setup

def load_description(*args):
    with open(str(args[0])) as file:
        return file.read()


NAME = "Skyforce"
AUTHOR = "Aaron Ma"
VERSION = "0.1.0"
SHORT_DESCRIPTION = "Skyforce provides stable implementations of various Python functions."
LONG_DESCRIPTION = load_description("README.md")

setup(
    name = NAME,
    version = VERSION,
    author = AUTHOR,
    description = SHORT_DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    # Not sure if PyPi support bitbucket yet.
    # url = "https://github.com/aaronhma/mathly",
    keywords = ["python", "skyforce"],
    include_package_data = True,
    # TODO(aaronhma): Uncomment next line
    packages = ["skyforce"],
    classifiers = [
        "License :: OSI Approved :: MIT License"
    ],
    license = "MIT"
)