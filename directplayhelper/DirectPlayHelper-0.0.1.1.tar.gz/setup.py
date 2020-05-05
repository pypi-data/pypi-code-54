import setuptools

setuptools.setup(
        name="DirectPlayHelper",
        version="0.0.1.1",
        author="Keivn Davis",
        author_email="kevincarrolldavis@gmail.com",
        scripts=["DirectPlayHelper/__main__.py"],
        description="Server and Client application for DirectPlay" +
                    "communication",
        long_description="Longer description",
        url="https://github.com/kevincar/DirectPlayHelper",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
            ]
        )
