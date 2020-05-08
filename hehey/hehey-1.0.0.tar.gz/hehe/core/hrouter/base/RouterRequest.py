# -*- coding: utf-8 -*-
import sys
from urllib import parse
from ..utils import CommonUtil

"""
 * 路由请求基类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class RouterRequest():

    '''
    :type router: hehe.core.hrouter.base.BaseRouter.BaseRouter
    '''

    def __init__(self,**attrs):

        self.url = '';
        self.params = {}
        self.environ = {}
        self.router = None;

        if attrs:
            CommonUtil.setAttrs(self,attrs)

        return ;


    def setEnviron(self,environ):

        self.environ = environ

        return ;

    def getPathinfo(self):

        path_info = self.environ['PATH_INFO'];

        return path_info.lstrip('/')

    def getMethod(self):

        return self.environ.get('REQUEST_METHOD','get').lower()

    def setRequestResult(self,result):

        if result:
            self.url = result[0];
            self.params = result[1]

        return ;

    def setRouter(self,router):

        self.router = router;

        return ;

    def buildUrl(self, url = '', vars = {},**options):

        return self.router.buildUrL(url,vars,self,**options);

    def parseRequest(self):

        return self.router.parseRequest(self);

    def getRouteUrl(self):

        return self.url

    def getRouteParams(self):

        return self.params



"""
 * url路由web请求类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class WebRouterRequest(RouterRequest):

    def getPathinfo(self):

        path_info = self.environ['PATH_INFO'];

        return path_info.lstrip('/')


"""
 * url路由控制器台请求类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class ConsoleRouterRequest(RouterRequest):


    def __init__(self,environ = {}):

        super().__init__(environ)

        url = sys.argv[1]
        result = parse.urlparse(url)

        self.environ['PATH_INFO'] = result.path
        self.environ['QUERY_STRING'] = result.query

        return

    def getPathinfo(self):

        path_info = self.environ['PATH_INFO'];

        return path_info.lstrip('/')

