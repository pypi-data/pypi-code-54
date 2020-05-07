import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="fact_wumian",
        version="0.0.1",
        author="wumian zhao",
        author_email="hhh@joke.com",
        url="https://baidu.com",
        long_description=long_description,
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3"
        ],
)
