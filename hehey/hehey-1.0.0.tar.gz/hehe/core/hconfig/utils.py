# -*- coding: utf-8 -*-
import importlib,os

"""
 * 类帮助类
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
    def getClassMeta(cls,clazz):

        if type(clazz) == str:
            packageClass = clazz.rsplit('.', 1)
            packageMeta = importlib.import_module(packageClass[0])
            return  getattr(packageMeta, packageClass[1])
        else:
            return clazz

    # 获取指定文件的扩展名
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getFileExt(self, filename):

        filelist = os.path.splitext(filename)
        ext = filelist[len(filelist) - 1]
        if ext:
            ext = ext[1:]

        return ext

    # 首字母大写
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def ucfirst(self, str):

        return str[0].upper() + str[1:]
