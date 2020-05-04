import io
from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


def read(*filenames, **kwargs):
    """ Read contents of multiple files and join them together """
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


pkg_info = {}
exec(read("kanjidb_anki/__version__.py"), pkg_info)


setup(
    name="kanjidb-anki",
    version=pkg_info["__version__"],
    author=pkg_info["__author__"],
    author_email=pkg_info["__author_email__"],
    url=pkg_info["__url__"],
    project_urls={
        "Bug Tracker": "https://github.com/Nauja/kanjidb-anki/issues",
        "Source Code": "https://github.com/Nauja/kanjidb-anki/",
    },
    description="Anki plugins for KanjiDB",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "kanjidb.builder.plugins": "ankideck = kanjidb_anki.builder.plugins.ankideck"
    },
    install_requires=["genanki"],
    test_suite="test",
    tests_require=["nose", "nose-cover3"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
)
