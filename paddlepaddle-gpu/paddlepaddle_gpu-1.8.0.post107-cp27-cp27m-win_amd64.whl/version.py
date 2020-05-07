# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.8.0'
major           = '1'
minor           = '8'
patch           = '0'
rc              = '0'
istaged         = False
commit          = '0231f58e592ad9f673ac1832d8c495c8ed65d24f'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
