# -*- coding: utf-8 -*-
import importlib

"""
 * 帮助类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class CommonUtil:


    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def setAttrs(cls,object,attrDict = {}):
        for attr in attrDict:
            setattr(object, attr, attrDict[attr])


    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getClassMeta(cls,clazz):
        if type(clazz) == str:
            packageClass = clazz.rsplit('.', 1)
            packageMeta = importlib.import_module(packageClass[0])
            classMeta = getattr(packageMeta, packageClass[1])
            return classMeta

        else:
            return clazz


    # 首字母大写
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def ucfirst(self,str):

        return str[0].upper() + str[1:]



