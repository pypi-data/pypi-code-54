# -*- coding: utf-8 -*-
from .utils.CommonUtil import CommonUtil
from .base.BaseLangPackage import BaseLangPackage
from .base.DefaultLangPackage import DefaultLangPackage

"""
 * 语言包管理
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class I18n:


    def __init__(self,**attrs):

        # 当前语言类型
        self.lang = ''
        # 语言包配置
        self.packages = {};

        # 语言包对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._langPackages = {}

        if attrs:
            CommonUtil.setAttrs(self,attrs)

        return ;

    # 获取语言消息
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getMessage(self,name,params = {},packageName = None,lang = None):

        packageName,name = self._buildLangPackageName(name,packageName);
        langPackage = self.getLangPackage(packageName);

        if lang is None:
            lang = self.lang


        return langPackage.getLangMessage(name,params,lang)

    def setLang(self,lang):

        self.lang = lang

    # 构建包名
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def _buildLangPackageName(self,name,packageName):

        pos = name.find(':')
        if pos == -1:
            return [name,packageName]
        else:
            packageName = name.rsplit(':',1)
            return [packageName[0], packageName[1]]

    # 获取指定语言包对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getLangPackage(self,packageName)->'BaseLangPackage':

        langPackage = self._langPackages.get(packageName,None);
        if langPackage is not None:
            return langPackage;

        packageConf = self.packages.get(packageName,None);
        if packageConf is None:
            raise Exception("i18n name {0} not find".format(packageName))

        langPackageClazz = packageConf.get("clazz",None)
        if langPackageClazz is None:
            langPackageClazz = DefaultLangPackage
        else:
            packageConf.pop('clazz')


        langPackageMeta = CommonUtil.getClassMeta(langPackageClazz)

        return langPackageMeta(**packageConf)



