import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covdata",
    version="1.1.5",
    author="Dripta senapati",
    author_email="driptasenapati97@gmail.com",
    description="A package that can grab all data of Covid-19 cases in India",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kalyaniuniversity/covidindia",
    packages=setuptools.find_packages(exclude=[]),
    include_package_data=True,
        package_data={
            'SERVER/templates': [
                'SERVER/templates/index_demo.html',
                'SERVER/templates/index_graph.html',
                'SERVER/templates/index_home.html',
                'SERVER/templates/index_rank.html',
                'SERVER/templates/index_state.html'
            ],
            'SERVER/static': [
                'SERVER/static/demo.js',
                'SERVER/static/graph.js',
                'SERVER/static/main.js',
                'SERVER/static/rank.js',
                'SERVER/static/state.js',
                'SERVER/static/style.css',
                'SERVER/static/style_demo.css',
                'SERVER/static/style_graph.css',
                'SERVER/static/style_rank.css',
                'SERVER/static/style_state.css'
            ],
    },
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.1',
        'matplotlib>=3.1.3',
        'datetime',
        'flask>=1.1.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "covdata=covdata.cli:main",
        ]
    },
    python_requires='>=3.6',
)
