import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auth-token",
    version="0.0.3",
    author="Jose Salas",
    author_email="josephsalas.developer@gmail.com",
    description="Auth token jwt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/developerjoseph/auth-token",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyjwt>=1.7.1'
    ]
)
