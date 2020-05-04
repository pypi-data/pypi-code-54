
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='mydream',  
     version='0.3.1',
     author="Jack Ma",
     script="mydream",
     author_email="924756831@qq.com",
     description="A man made Easter-Egg",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/kingjacM",
     packages=["mydream"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],


 )