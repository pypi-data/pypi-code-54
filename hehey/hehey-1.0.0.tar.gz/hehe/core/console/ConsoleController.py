# -*- coding: utf-8 -*-
"""
 * 控制器基类
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

from hehe.core.base.BaseController import BaseController
from hehe import he

class ConsoleController(BaseController):

    def actions(self):

        return ;

    def beforeAction(self):

        return True;

    def validate(self,dataList = None,rules = [] ,scenes = {},clearErrors = True):

        return he.app.validation.validate(dataList,rules,scenes,clearErrors);


    def query(self,name = None,defaultValue = None):

        return he.app.hrequest.getQuery(name,defaultValue);

    def request(self,name = None,defaultValue = None):

        return he.app.hrequest.getRequest(name,defaultValue);

    # 标准输出
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def stdout(self,chars):

        return ;

    # 标准错误
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def stderr(self,chars):

        return ;


