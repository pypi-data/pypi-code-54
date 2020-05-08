# -*- coding: utf-8 -*-
import importlib,inspect

"""
 * 帮助类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class CommonUtil:

    BEAN_REF_REGEX = r'<ref::([^>]+)?>'
    PARAMS_REGEX = r'<(.+)::([^>]+)?>'

    # 获取类或对象的自定义属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getAttrs(cls,object):
        attrs = dir(object);
        attrDict = {};
        for attr in attrs:
            if not attr.startswith("__"):
                attrDict[attr] = getattr(object,attr)

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
    def getModuleMeta(cls,clazz):

        packageClass = clazz.rsplit('.', 1)
        packageMeta = importlib.import_module(packageClass[0])
        #
        return  getattr(packageMeta, packageClass[1])


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

    # 获取类或方法的完整包名
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getClassName(cls, clazz):

        clazzModule = inspect.getmodule(clazz);
        clazzName = clazzModule.__name__ + '.' + clazz.__class__.__name__

        return clazzName

    # 构建bean 定义配置
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def buildBeanDefinition(cls,beanId,beanClazzMeta,definition):

        clazzModule = inspect.getmodule(beanClazzMeta).__name__;
        clazzBean = clazzModule + '.' + beanClazzMeta.__name__
        beanConf = {
            'clazz': clazzBean,
        }

        if beanId:
            beanConf['id'] = beanId
        else:
            beanConf['id'] = clazzBean

        beanConf.update(definition)

        return beanConf;

    # 构建ref bean 定义配置
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def buildRefDefinition(self,beanId,propertyMeta,definition):

        beanDefinition = definition.copy();

        clazzModule = inspect.getmodule(propertyMeta).__name__
        clazzBean = clazzModule + '.' + propertyMeta.__qualname__.split('.')[0];
        propertyName = propertyMeta.__name__;
        beanDefinition['clazz'] = clazzBean
        realName = definition.pop('name', None)
        if realName:
            beanDefinition[realName] = '<ref::' + beanId + '>'
        else:
            beanDefinition['__' + propertyName] = '<ref::' + beanId + '>'

        return beanDefinition;

