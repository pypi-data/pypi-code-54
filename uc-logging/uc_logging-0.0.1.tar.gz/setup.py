# -*- coding: utf-8 -*-
# uc_logging - A set of classes and functions that extend the log package.
# It is part of the Unicon project.
# https://unicon.10k.me
#
# Copyright © 2020 Eduard S. Markelov.
# All rights reserved.
# Author: Eduard S. Markelov <markeloveduard@gmail.com>
#
# This program is Free Software; you can redistribute it and/or modify it under
# the terms of version three of the GNU Affero General Public License as
# published by the Free Software Foundation and included in the file LICENSE.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
The build script for setuptools.
"""
import setuptools


with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


setuptools.setup(
    name="uc_logging",
    version="0.0.1",
    author="Eduard S. Markelov",
    author_email="markeloveduard@gmail.com",
    description="A set of classes and functions that extend the log package.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dentist128/uc_logging",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "logging"
    ],
    python_requires='>=3.4, <4',
)
