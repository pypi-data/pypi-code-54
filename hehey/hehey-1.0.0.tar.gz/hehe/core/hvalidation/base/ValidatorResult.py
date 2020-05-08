# -*- coding: utf-8 -*-

"""
 * 验证器验证结果类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""

class ValidatorResult(object):

    def __init__(self,result,message = '',params = {}):

        # 验证结果
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.result  = False

        # 验证结果返回的其他参数
        # <B> 说明： </B>
        # <pre>
        # 用于
        # </pre>
        self.params = {};

        # 错误提示消息
        # <B> 说明： </B>
        # <pre>
        # 用于
        # </pre>
        self.message = '';

        self.result = result
        self.params = params
        self.message = message

    def getMessage(self):

        return self.message

    def getParams(self):

        return self.params

    def getResult(self):

        return self.result

    def setResult(self,result = False):

        self.result = result
