import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytwitchplays",
    version="0.1.0",
    author="Benjamin Janssens",
    author_email="benji.janssens@gmail.com",
    description="Python package to create your own Twitch Plays channel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benjiJanssens/PyTwitchPlays",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pytwitchchat',
    ]
)
