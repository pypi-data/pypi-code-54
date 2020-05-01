from setuptools import setup
 
NAME = 'Mydemos_pkg'
VERSION = '1.1.4.0'
PACKAGES = ['Mydemos_pkg']
setup(name = NAME
        , version = VERSION
        , packages = PACKAGES,
      description='a small pkg demos for you and everyone',
      long_description='''
```shell
pip install Mydemos_pkg
```
'''
      ,long_description_content_type='text/markdown'
) 
