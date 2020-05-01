from distutils import log
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist as _sdist

import os
from glob import glob
import shutil


def remove(path):
    """ param <path> could either be relative or absolute. """
    log.info("removing " + path)
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


class SDist(_sdist):
    def run(self):
        self.run_command("build_ext")
        _sdist.run(self)


def find_files(base="algopack", extension="*"):
    return glob(os.path.join(base, "**", "*." + extension), recursive=True)


class Clean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        remove("build")
        for folder in glob("*.egg-info"):
            remove(folder)
        for pyd_file in find_files(extension="pyd"):
            remove(pyd_file)
        for so_file in find_files(extension="so"):
            remove(so_file)

        pyx_files = find_files(extension="pyx")

        c_files = find_files(extension="c")
        for c_file in c_files:
            if c_file[:-2] + ".pyx" in pyx_files:
                remove(c_file)

        cpp_files = find_files(extension="cpp")
        for cpp_file in cpp_files:
            if cpp_file[:-4] + ".pyx" in pyx_files:
                remove(cpp_file)


try:
    from Cython.Distutils.extension import Extension
    from Cython.Distutils import build_ext
except ImportError:
    from setuptools import Extension

    USING_CYTHON = False
else:
    USING_CYTHON = True


ext_modules = [
    {"path": ("algopack", "sort")},
    {"path": ("algopack", "stack"), "language": "c++"},
]


extension_kwargs = (
    dict(cython_directives={"language_level": 3, "embedsignature": True})
    if USING_CYTHON
    else dict()
)


def create_extension(module):
    global USING_CYTHON, extension_kwargs

    name = ".".join(module["path"])
    path = os.path.join(*module["path"])
    language = module.get("language", "c")
    multisource = module.get("multisource", False)

    if USING_CYTHON:
        extension = "pyx"
    elif language == "c":
        extension = "c"
    elif language == "c++":
        extension = "cpp"

    if multisource:
        sources = find_files(path, extension)
    else:
        sources = [path + "." + extension]

    return Extension(name, sources, language=language, **extension_kwargs)


cmdclass = {"build_ext": build_ext, "sdist": SDist} if USING_CYTHON else {}
cmdclass["clean"] = Clean

with open("requirements.txt") as fp:
    install_requires = [line.strip() for line in fp if line.strip()]

with open("requirements_dev.txt") as fp:
    dev_requires = [line.strip() for line in fp if line.strip()]

if __name__ == "__main__":
    setup(
        packages=find_packages(exclude=("tests")),
        ext_modules=[create_extension(module) for module in ext_modules],
        cmdclass=cmdclass,
        install_requires=install_requires,
        extras_require={"dev": dev_requires},
    )
