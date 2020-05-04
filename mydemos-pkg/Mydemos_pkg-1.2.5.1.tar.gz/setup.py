from setuptools import setup
 
NAME = 'Mydemos_pkg'
VERSION = '1.2.5.1'
PACKAGES = ['Mydemos_pkg']
setup(name = NAME
        , version = VERSION
        , packages = PACKAGES,
      description='a small pkg demos for you and everyone',
      long_description='''
```shell
pip install Mydemos_pkg
```
~~lastest_version~~

OK,I will have a list for the version that released.


1.0.1.1

1.1.1.0

1.1.3.0

1.1.4.0

1.2.1.0

1.2.3.0

1.2.3.1


1.2.4.0

1.2.5.1
```py
\'\'\'
USAGE
\'\'\'
from Mydemos_pkg.nim import nim
nim()
from Mydemos_pkg.sort import sort_test
sort_test()
```
so it's that.......
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

'''
      ,long_description_content_type='text/markdown'
) 
