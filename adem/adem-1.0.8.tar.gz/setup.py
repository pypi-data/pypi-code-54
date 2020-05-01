from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('HISTORY.md') as hf:
    HISTORY = hf.read()

setup_args = dict(
                name="adem",
                version="1.0.8",
                author="Miracle Adebunmi",
                author_email="miraclem2014@gmail.com",
                description="Giving Python Ability to Work directly on Matrices explicitly",
                long_description=long_description +'\n\n' + HISTORY,
                license = 'MIT',
                long_description_content_type="text/markdown",
                url="https://github.com/miracle5284/adem",
                packages = find_packages(),
                classifiers = [
                                "Programming Language :: Python :: 3",
                                "License :: OSI Approved :: MIT License",
                                "Operating System :: OS Independent",
                              ],
                python_requires ='>=3.6',
                
)

requirements = [
    'numpy>=1.6.0'
    ]

if __name__ == '__main__':
    setup(**setup_args,install_requires = requirements)
