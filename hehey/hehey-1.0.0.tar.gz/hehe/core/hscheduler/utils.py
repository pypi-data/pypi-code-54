# -*- coding: utf-8 -*-
import importlib

"""
 * 任务调度帮助类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
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
    def getAttrs(cls, object):

        attrs = object.__dict__;
        attrDict = {};
        for attr in attrs:
            if not attr.startswith("_"):
                attrDict[attr] = getattr(object, attr)

        return attrDict

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getAttrValues(cls, object,attrNames = []):

        attrDict = {};
        for attrName in attrNames:
            attrDict[attrName] = getattr(object, attrName)

        return attrDict

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def setAttrs(cls,object,attrDict = {}):

        for attr in attrDict:
            setattr(object, attr, attrDict[attr])

    def splitClassName(clazz):

        packageClass = clazz.rsplit('.', 1)

        return [packageClass[0],packageClass[1]]

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
            return  getattr(packageMeta, packageClass[1])
        else:
            return clazz

    # 首字母大写
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def ucfirst(cls, str):

        return str[0].upper() + str[1:]

