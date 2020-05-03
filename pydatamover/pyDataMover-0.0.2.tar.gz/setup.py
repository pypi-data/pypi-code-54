"""


"""

import os
import os.path
import re
import sys
import distutils.cmd
import setuptools
from   setuptools import setup, Extension, find_packages
from   setuptools.command.build_ext import build_ext
from   setuptools.command.test import test as TestCommand

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(DIR_PATH, 'README.md'), encoding='utf-8') as f:
    LONG_DESC = f.read()

print(LONG_DESC)
class CleanCommand(distutils.cmd.Command):
    """
    Our custom command to clean out junk files.
    """
    description = "Cleans out junk files we don't want in the repo"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cmd_list = dict(
            DS_Store=f"find {DIR_PATH} -name .DS_Store -type d -print0 | xargs -0 rm -Rf;",
            so_files=f"find {DIR_PATH} -name '*.so' -type f -print0 | xargs -0 rm -f;",
            pycache=f"find {DIR_PATH} -name __pycache__ -type d -print0 | xargs -0 rm -Rf;",
            pyc=f"find {DIR_PATH} -name '*.pyc' -exec rm -rf {{}} \;",
            build_dir=f"rm -Rf {DIR_PATH}/build",
            folly_dir=f"rm -Rf {DIR_PATH}/folly",
            tmp_dir=f"rm -Rf {DIR_PATH}/tmp/*",
            htmlcov=f"rm -Rf {DIR_PATH}/htmlcov",
            htmlcov_test=f"rm -Rf {DIR_PATH}/tests/htmlcov",
        )
        for key, cmd in cmd_list.items():
            os.system(cmd)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', '--cov=', 'pyDataMover') ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov', 'pyDataMover', '--cov-report', 'html', '--verbose', '--verbose']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

with open(os.path.normpath(os.path.join(DIR_PATH, 'src', 'pyDataMover', '__init__.py'))) as f:
    VERSION = re.search(
        r'^__version__\s*=\s*["\']([0-9ab.]+)["\']',
        f.read(), re.MULTILINE|re.VERBOSE).group(1)


class GetPyBindInclude():
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def includes(self):
        """Return pybind11 include dir's"""
        import pybind11
        return pybind11.get_include(self.user)
    def __str__(self):
        return self.includes()

EXT_MODULES = [
    Extension(
        'pyDataMover/_pyDataMover',
        ['src/pyDataMover/_pyDataMover.cpp'],
        libraries=[
            'datamover',
            'ssl',
        ],
        include_dirs=[
            # FIXME
            "src/pyDataMover",
            "folly",
            "/var/tmp/dm_install/usr/local/include", #"/usr/local/DataMover/include",
            "/usr/include/boost169",
            GetPyBindInclude(),
            GetPyBindInclude(user=True),
        ],
        library_dirs=[
            #FIXME
            "/var/tmp/dm_install/usr/local/lib64", #"/usr/local/DataMover/lib64",
            "/usr/lib64/boost169",
        ],
        language='c++'
    ),
]


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as tfh:
        tfh.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([tfh.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++14 compiler flag.

    Forcing c++14.
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': ['-DNDEBUG'],
    }


    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        #os.system("git clone https://github.com/facebook/folly.git")
        comp_type = self.compiler.compiler_type
        opts = self.c_opts.get(comp_type, [])
        if comp_type == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif comp_type == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)

setup(
    name='pyDataMover',
    version=VERSION,
    author='Chris Majoros',
    author_email='chris@majoros.us',
    url='https://github.com/majoros/pyDataMover',
    description='Python wrapper for the Facebook wdt library.',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    long_description=LONG_DESC,
    ext_modules=EXT_MODULES,
    install_requires=['pybind11>=2.2'],
    cmdclass={
        'build_ext': BuildExt,
        'test': PyTest,
        'clean': CleanCommand,
    },
    zip_safe=False,
    tests_require=['pytest'],
)
