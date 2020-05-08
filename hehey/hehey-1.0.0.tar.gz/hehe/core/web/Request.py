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

class Request:


    def __init__(self,environ):
        self.GET = {};
        self.POST = {}
        self.environ = environ
        self.cookies = {}

        self.init()


    def init(self):
        # 解析参数
        self.GET = urllib.parse.parse_qs(self.environ.get('QUERY_STRING', ''))

        # cookie 解析
        http_cookie = str(self.environ.get('HTTP_COOKIE', ''))
        if http_cookie:
            http_cookieList = http_cookie.split(';')
            for cookie in http_cookieList:
                cookieArr = cookie.split('=')
                self.cookies[cookieArr[0].strip()] = cookieArr[1]


    def getCookie(self,name,defaultValue = None):

        return self.cookies.get(name,defaultValue)

    def getCookies(self):

        return self.cookies

    def query(self,name,default = [None]):
        return self.GET.get(name, default)[0]


    def get(self,name,default = [None]):
        return self.GET.get(name, default)[0]

    def getMethod(self):
        return 'get'

    def getEnviron(self):
        return self.environ

    def mergeGet(self,params = {}):
        self.GET.update(params)

