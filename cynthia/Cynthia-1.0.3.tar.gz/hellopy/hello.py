# -*- coding: utf-8 -*-

# Author: Cynthia

"""
    测试自定义包访问内部子包
"""
# 这里注意, 作为一个工程的时候, 用相对路径是没问题的
# 但是如果是作为一个包, __main__指不定在哪个路径, 此时再用相对路径就不合适了
# 有两个办法, 一个是修改__init__.py, 导包的时候把路径加到sys.path里去
# 另一个是一律用全绝对路径, 即从基包hellopy开始, 还可以更好避免命名冲突, 建议方案2
import hellopy.opts.const as oc
import hellopy.utils.tool as ut

def f():
    print(oc.lines)
    ut.f()

if __name__ == '__main__':
    f()