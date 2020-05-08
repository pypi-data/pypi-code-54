# -*- coding: utf-8 -*-
"""
 * action 基类
 *<B>说明：</B>
 *<pre>
 *  略
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

from hehe.core.web.WebController import WebController
from hehe import he
from hehe.helper.ClassHelper import ClassHelper

class BaseAction(WebController):

    def __init__(self):

        super().__init__()

        self.method = 'GET';

    def _init(self):

        self.load();

        return ;

    # 获取对象属性名称列表
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def setAttributes(self,values):

        if values:
            attrs  = self.attributes()
            for attrName in attrs:
                value = values.get(attrName,None)
                if value is not None:
                    setattr(self,attrName,value)

        return ;

    # 获取对象属性名称列表
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def attributes(self):

        attrs = ClassHelper.getAttributes(self);

        return attrs.keys();


    # 获取对象的属性值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getAttributes(self,names = None,exclude = None):

        values = {};
        if names is None:
            names = self.attributes();

        for name in names:
            values[name] = getattr(self,name)

        if exclude:
            for name in exclude:
                values.pop(name);

        return values;

    # 客户端数据加载至action 属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def load(self,data = {}, method = ''):

        if not data:
            if not method:
                method = self.method

            if method == 'POST':
                data = he.app.hrequest.post
            elif method == 'GET':
                data = he.app.hrequest.query;
            else:
                data = he.app.hrequest.request;

        self.setAttributes(data);

        return ;

    def validate(self, scenes = {},rules = [], clearErrors = True):

        if not rules:
            rules = self.rules();

        return he.app.validation.validate(self, rules, scenes, clearErrors);

    def rules(self):

        return []