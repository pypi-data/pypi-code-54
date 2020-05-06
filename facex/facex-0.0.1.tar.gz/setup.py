import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="facex", # Replace with your own username
    version="0.0.1",
    author="Hasby Fahrudin",
    author_email="fahrudinhasby12@gmail.com",
    description="Facial Expression Classifier API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hfahrudin/facex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'tensorflow>=2.0.0',
        'scikit-image>=0.16.2'
    ],
    python_requires='>=3.6',
)
