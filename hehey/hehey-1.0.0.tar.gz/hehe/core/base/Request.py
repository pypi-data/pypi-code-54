# -*- coding: utf-8 -*-

"""
 * 请求类
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
import urllib
import uuid

class Request:

    def __init__(self):

        self.environ = {};

        # 每个请求自动生成唯一id
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.reqid = str(uuid.uuid1())

        self._GET = {};

    def initEnviron(self,environ):

        self.environ = environ

        self._GET = {};

    def getEnviron(self):

        return self.environ



    # 获取请求pathInfo
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getPathInfo(self):

        return self.environ.get('PATH_INFO');

    def getRequestId(self):

        return self.reqid;


