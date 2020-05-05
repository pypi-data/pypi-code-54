# ===============================================================================
#
# This file is part of the gdecomp package.
#
# gdecomp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
#
# ===============================================================================
# Binding of Guassian Decompostion function
# Creation date: 2019-05-24
# Author: Florian de Boissieu
from setuptools import setup, Extension, find_packages

# Adapted from https://github.com/pybind/python_example/blob/master/setup.py
# See https://stackoverflow.com/questions/54117786/add-numpy-get-include-argument-to-setuptools-without-preinstalled-numpy
class get_numpy_include(str):
    """Helper class to determine the numpy include path
    The purpose of this class is to postpone importing numpy
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __str__(self):
        import numpy
        return numpy.get_include()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gdecomp',
    description="Gaussian Decompostion of a LiDAR Waveform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pytools4dart/gdecomp",
    author="Florian de Boissieu",
    author_email="fdeboiss@gmail.com",
    license="GPLv3",
    version='1.0.5',
    classifiers=[
        # Project maturity:
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Execution environment
        'Environment :: Console',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',

        # License
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=("tests",)),
    setup_requires=['setuptools>=18.0', 'numpy', 'cython'],
    install_requires=['numpy', 'cython'],
    # cythonize not needed: https://stackoverflow.com/questions/37471313/setup-requires-with-cython
    ext_modules=[Extension("gdecomp",
                       ["src/mpfit/mpfit.c",
                        "src/PulseGaussianFitting.cpp",
                        "src/gdecomp.pyx"],
                       include_dirs=[get_numpy_include(), 'src', 'src/mpfit'],
                       language='c++',
                       extra_compile_args=["-std=c++11"],
                       extra_link_args=["-std=c++11"]
                       )],
)

