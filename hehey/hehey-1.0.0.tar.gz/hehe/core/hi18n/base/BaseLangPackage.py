# -*- coding: utf-8 -*-
from ..utils.CommonUtil import CommonUtil

"""
 * 语言包基类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class BaseLangPackage:

    def __init__(self,**attrs):

        # 语言包消息
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.messages = {};

        # 语言包文件路径
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.packagePath = '';

        # 文件列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.files = [];

        # 配置扩展名对应的处理方法
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.extHandler = {
            'py':self._pyHandler,
            'ini':self._iniHandler,
            'yaml':self._yamlHandler,
            'json':self._jsonHandler,
            'xml': self._xmlHandler
        }

        if attrs:
            CommonUtil.setAttrs(self,attrs)

        return ;

    # 获取指定key的语言message
    # <B> 说明： </B>
    # <pre>
    # 文件
    # </pre>
    def getLangMessage(self,name,params = {},lang = ''):

        packagePath = self.buildLangPackagePath(lang);
        self.loadLangPackage(packagePath);
        message = self.getMessage(name)

        return self.formatMessage(message,params)

    # 构建包路径地址
    # <B> 说明： </B>
    # <pre>
    # 文件
    # </pre>
    def buildLangPackagePath(self,lang):

        if lang:
            return self.packagePath + '/' + lang
        else:
            return self.packagePath


    # 导入包文件
    # <B> 说明： </B>
    # <pre>
    # 文件
    # </pre>
    def loadLangPackage(self,packagePath = ''):

        if self.messages:
            return True

        messages = {}
        # 读取文件信息
        for file in self.files:
            filepath = packagePath + '/' + file
            message = self.getPackageMessages(filepath);
            if message:
                messages.update(message);

        self.messages = messages;

    def getMessage(self,name:str):

        nameList = name.split('.');
        messages = self.messages;
        message = '';
        for name in nameList:
            msg = messages.get(name,None)
            if msg is None:
                # 字典 key 不存在,中断返回
                message = None;
                break;
            else:
                messages = msg;
                message = msg;

        return message;

    # 获取包数据
    # <B> 说明： </B>
    # <pre>
    # 文件
    # </pre>
    def getPackageMessages(self,filepath)->'dict':

        ext = CommonUtil.getFileExt(filepath);
        handler = self.extHandler.get(ext,self._pyHandler)

        return handler(filepath);

    def _pyHandler(self,filepath):

        with open(filepath, 'r') as f:
            packageFileCode = f.read()

        params = {
            "lang": {}
        };

        exec(packageFileCode, params)

        return params['lang']

    def _iniHandler(self,filepath):

        import configparser;
        cf = configparser.ConfigParser()
        cf.read(filepath, encoding='utf8')

        items = dict(cf._sections)
        messages = {}

        for key in items:
            messages[key] = dict(items[key])

        # 读取其他配置文件
        return messages;

    def _yamlHandler(self,filepath):
        import yaml
        messages = {}
        with open(filepath, 'r') as f:
            messages = yaml.full_load(f.read())

        return messages

    def _jsonHandler(self,filepath):
        import json
        messages = {}
        with open(filepath, 'r') as f:
            messages = json.load(f)

        return messages

    def _xmlHandler(self,filepath):

        from ..utils import XmlUtil
        messages = XmlUtil.toDic(filepath)

        return messages


    def formatMessage(self,message,params = {}):

        return message.format(**params)