import setuptools

def obtain_version():
    def version_scheme(version):
        return version.format_with("{tag}")

    def local_scheme(version):
        if version.exact:
            metadata = \
                version.format_choice(
                    clean_format="",
                    dirty_format="+dirty"
                )
        else:
            metadata = "+" + version.node[1:]
            metadata = \
                version.format_choice(
                    clean_format=metadata,
                    dirty_format=metadata + ".dirty"
                )
        return metadata

    return {
        "version_scheme": version_scheme,
        "local_scheme": local_scheme,
    }

with open("README.md", "r") as description_file:
    long_description = description_file.read()

setuptools.setup(
    name="rockart-examples",
    use_scm_version=obtain_version,
    description="Collection of Rockart usage examples",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="pseudographics semigraphics braille terminal console",
    license="MIT",
    author="van-kalsing",
    author_email="kalsin@inbox.ru",
    url="https://github.com/van-kalsing/rockart-examples",
    project_urls={
        "Bug Tracker": "https://github.com/van-kalsing/rockart-examples/issues",
        "Source Code": "https://github.com/van-kalsing/rockart-examples",
    },
    zip_safe=True,
    packages=["rockart_examples"],
    entry_points={
        "console_scripts": [
            "rockart-life = rockart_examples.life.entry:entry",
        ],
    },
    python_requires=">=3.6.9",
    install_requires=["rockart==0.2.*"],
    setup_requires=["setuptools_scm==3.2.0"],
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Terminals",
    ],
)
