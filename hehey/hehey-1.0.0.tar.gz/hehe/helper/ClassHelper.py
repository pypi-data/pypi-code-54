# -*- coding: utf-8 -*-
import importlib,inspect,random,time,hashlib
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('安全伪随机数生成器不可用')
    using_sysrandom = False

"""
 * 类帮助类
 *<B>说明：</B>
 *<pre>
 *  提供基本类操作,获取属性值,设置属性等等
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
 *<B>日志：</B>
 *<pre>
 *  略
 *</pre>
 *<B>注意事项：</B>
 *<pre>
 *  略
 *</pre>
"""
class ClassHelper:

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @staticmethod
    def getAttrs(object):
        attrs = dir(object);
        attrDict = {};
        for attr in attrs:
            if not attr.startswith("__"):
                attrDict[attr] = getattr(object,attr)

        return attrDict

    @classmethod
    def getAttributes(cls, object):
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
    @staticmethod
    def setAttrs(object,attrDict = {}):
        for attr in attrDict:
            setattr(object, attr, attrDict[attr])

    # 获取上一级目录
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def dirname(cls,clazz):
        packageClass = clazz.rsplit('.', 1)
        return packageClass[0];

    # 首字母大写
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def ucfirst(self, str):
        return str[0].upper() + str[1:]

    # 首字母小写
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def lcfirst(self, str):

        return str[0].lower() + str[1:]


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

    # 获取类或方法的完整包名
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getModuleName(cls,module):

        currentModule = inspect.getmodule(module)
        if currentModule.__name__ == '__main__':
            moduleName = module.__qualname__
        else:
            moduleName = currentModule.__name__ + '.' + module.__name__

        return moduleName


    def buildRandomString(length = 12,
                          allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        if not using_sysrandom:

            random.seed(
                hashlib.sha256(
                    ('%s%s%s' % (random.getstate(), time.time(), 'uuuu')).encode()
                ).digest()
            )

        return ''.join(random.choice(allowed_chars) for i in range(length))

    # md5 字符串
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def md5(cls,rawchars):


        return hashlib.md5(rawchars.encode(encoding='UTF-8')).hexdigest();