# -*- coding: utf-8 -*-
from ..base.Request import Request
from ..base.annotation import cached_property
from urllib import parse;
import sys
"""
 * 控制台请求类
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

class ConsoleRequest(Request):

    def mergeGet(self,params = {}):

        self.query.update(params)

    @cached_property
    def query(self)->'dict':

        self._parse_query_data();

        return self._GET;

    @cached_property
    def request(self)->'dict':

        self._parse_query_data()
        request = {};
        request.update(self._GET)

        return request;

    # 获取问号? 参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getQuery(self,name = None,defaultValue = None):

        if name is None:
            return self.query

        return self.query.get(name,defaultValue);

    # 获取request参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getRequest(self, name = None, defaultValue=None):

        if name is None:
            return self.request

        return self.request.get(name, defaultValue);


    def _parse_query_data(self):

        query = dict([(k, parse.unquote(v[0])) for k, v in parse.parse_qs(self.environ.get('QUERY_STRING', '')).items()]);

        _get = {};
        _get.update(query)
        _get.update(self._GET)

        self._GET = _get


    def __getattr__(self, name):

        return self.getRequest(name,'')














