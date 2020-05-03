from setuptools import setup
 
NAME = 'badwords'
VERSION = '1.2.4.0'
PY_MODULES = ['badwords']
setup(name = NAME
        , version = VERSION
        , py_modules = PY_MODULES,
      description='a small pkg demos for you and everyone',
      long_description='''
```shell
pip install badwords
```
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

'''
      ,long_description_content_type='text/markdown'
) 
