from setuptools import setup

# For instructions on how to make a package visit: https://www.youtube.com/watch?v=QgZ7qv4Cd0Y


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name= 'hwdean',
    version='0.0.7', 
    description="""A package for training and predicting temporal cell 
                    response predictions (tcrp) for florescent microscopy time-lapse data.""", 
    py_modules=["hwdean"], 
    url = 'https://bitbucket.astrazeneca.com/users/krjm801/repos/package_dev',   # Provide either the link to your github or to your website
    download_url = 'https://bitbucket.astrazeneca.com/users/krjm801/repos/package_dev/browse/dist/hwdean-0.0.7.tar.gz',    # I explain this later on
    package_dir={'':'src'}, 
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    classifiers=["Programming Language :: Python :: 3.8", 
                "License :: OSI Approved :: MIT License", 
                "Operating System :: OS Independent"], 
    author="Dean Sumner", 
    author_email="dean.sumner@astrazeneca.net", 
    license="MIT"

)

# This file should go outside of the source file... se hellowworld.py for the actual src code. 
# To build, from terminal in project dir (same place as setup.py) 

# $ python setup.py bdist_wheel 
# $ python setup.py sdist
# $ git add 
# $ git commit
# $ git push
# $ check-manifest (makes sure you have your files git tracked)
# $ check-manifest --create
# $ git add MANIFEST.in
# $ pipenv install --dev twine
# $ twine upload dist/*
