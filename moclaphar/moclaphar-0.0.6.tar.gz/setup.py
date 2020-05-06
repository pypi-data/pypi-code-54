import setuptools

setuptools.setup(
    name="moclaphar",
    version="0.0.6",
    license='MIT',
    author="Jongkuk Lim",
    author_email="lim.jeikei@gmail.com",
    description="This packages mainly aims to make an easy process for dataset manipulation.",
    long_description=open('README.md').read(),
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
