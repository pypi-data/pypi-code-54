# -*- coding: utf-8 -*-
from ..base.Request import Request
from ..base.annotation import cached_property
from .Cookies import Cookies
from .Headers import Headers
import re;
from urllib import parse;
import sys
from .wsgihttp import WsgiHttpParser;

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

class WebRequest(Request):

    def __init__(self):

        super().__init__()

        self.charset = 'utf-8';

        return ;

    def mergeGet(self,params = {}):

        self.query.update(params)

    @cached_property
    def files(self)->'dict':

        self._parse_form_data()

        return self._FILES;

    @cached_property
    def cookies(self)->'Cookies':

        httpCookie = str(self.environ.get('HTTP_COOKIE', ''))
        cookies = Cookies()
        cookies.parseCookies(httpCookie)

        return cookies;

    @cached_property
    def headers(self):

        headers = Headers()
        for name in self.environ:
            if name[0:5] == 'HTTP_':
                headers.set(name,self.environ[name]);

        return headers;

    @cached_property
    def post(self)->'dict':

        self._parse_form_data()

        return self._POST;

    @cached_property
    def query(self)->'dict':

        self._parse_query_data();

        return self._GET;

    @cached_property
    def request(self)->'dict':

        self._parse_form_data()
        request = {};
        request.update(self._POST)
        request.update(self._GET)

        return request;

    # 返回content-type
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    @cached_property
    def contentType(self):

        contentType = self.environ.get("CONTENT_TYPE", "")
        contentTypeItems = contentType.split(';')
        contentType = contentTypeItems.pop(0);

        return contentType;

    # 获取请求method
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getMethod(self):

        return self.server('REQUEST_METHOD').upper();

    # 获取请求host
    # <B> 说明： </B>
    # <pre>
    # 包含端口
    # </pre
    def getHostInfo(self) -> 'str':

        host = self.getScheme() + '://';
        if self.getPort() == '80':
            host = host + self.server('HTTP_HOST').split(":")[0]
        else:
            host = host + self.server('HTTP_HOST')

        return host

    # 获取请求端口
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getPort(self):

        return self.server('SERVER_PORT').upper();

    # 获取远程ip 地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getRemoteAddr(self):

        return self.server('REMOTE_ADDR').upper();

    # 获取客户端ip
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getClentIp(self):

        if self.getHeader('HTTP_X_FORWARDED_FOR'):
            http_x_forwarded_for = self.getHeader('HTTP_X_FORWARDED_FOR').split(",");
            ip = http_x_forwarded_for[0];
        elif self.getHeader('HTTP_CLIENT_IP'):
            ip = self.getHeader('HTTP_CLIENT_IP')
        else:
            ip = self.getRemoteAddr()

        return ip;

    # 获取environ 参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def server(self,name,defaultValue = None):

        return self.environ.get(name,defaultValue);



    # 获取问号? 参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getQuery(self,name = None,defaultValue = None):

        if name is None:
            return self.query

        return self.query.get(name,defaultValue);

    # 获取post参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getPost(self, name = None, defaultValue=None):

        if name is None:
            return self.post

        return self.post.get(name, defaultValue);

    # 获取files参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getFiles(self, name = None, defaultValue=None):

        if name is None:
            return self.files

        return self.files.get(name, defaultValue);

    # 获取request参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getRequest(self, name = None, defaultValue=None):

        if name is None:
            return self.request

        return self.request.get(name, defaultValue);

    # 获取cookie参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getCookie(self,name = None, defaultValue=None):

        if name is None:
            return self.cookies

        return self.cookies.get(name,defaultValue)

    # 获取header参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getHeader(self, name=None, defaultValue=None)->'str':

        if name is None:
            return self.headers

        return self.headers.get(name, defaultValue)

    # 是否ajax 请求
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def isAjax(self):

        http_x_requested_with = self.headers.get('HTTP_X_REQUESTED_WITH')

        if http_x_requested_with is not None and http_x_requested_with == 'XMLHttpRequest':
            return True
        else:
            return False

    # 是否pjax 请求
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def isPjax(self):

        if self.isAjax() and self.server('HTTP_X_PJAX',None):
            return True
        else:
            return False

    # 是否POST 请求
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def isPost(self):

        return self.getMethod() == 'POST'

    # 是否get 请求
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def isGet(self):

        return self.getMethod() == 'GET'

    # 获取协议类型
    # <B> 说明： </B>
    # <pre>
    # http or https
    # </pre
    def getScheme(self):

        return self.server('wsgi.url_scheme')

    # 获取url 地址
    # <B> 说明： </B>
    # <pre>
    # 只包含路径,不包含域名
    # </pre
    def getUrl(self):

        return self.getPathInfo();

    # 获取完整的url 地址
    # <B> 说明： </B>
    # <pre>
    # 域名,端口,参数
    # </pre
    def getFullUrl(self):

        uri = self.getHostInfo() + self.getUrl()
        if self._GET:
            uri = uri + '?' + parse.urlencode(self._GET)

        return uri;


    def getHostUrl(self):

        uri = self.getHostInfo() + self.getUrl()

        return uri;



    # 获取原始body
    # <B> 说明： </B>
    # <pre>
    # 直接获取wsgi.input 值
    # </pre
    def getRawBody(self):

        return self.server('wsgi.input');


    def _parse_query_data(self):

        query = dict([(k, parse.unquote(v[0])) for k, v in parse.parse_qs(self.environ.get('QUERY_STRING', '')).items()]);

        _get = {};
        _get.update(query)
        _get.update(self._GET)

        self._GET = _get


    # 解析form 表单数据
    # <B> 说明： </B>
    # <pre>
    # form 表单数据,一般包含普通字段,上传的文件内容,数据流
    # </pre
    def _parse_form_data(self):

        if "_POST" in self.__dict__:
            return ;

        data = WsgiHttpParser(self.environ,self.charset).parse();

        d = self.__dict__

        d["_POST"], d["_FILES"] = data

        return ;


    def __getattr__(self, name):

        return self.getRequest(name,'')














