import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyextmath-selcukwashere", # Replace with your own username
    version="0.0.1",
    author="Selcuk Oz",
    author_email="selcukoz_2005@hotmail.com",
    description="A library for easier maths",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/selcukwashere/pyextmath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["numpy","pyautogui"]
)