# -*- coding: utf-8 -*-

from hehe.core.base.BaseApplication import BaseApplication
from hehe import he

"""
 * web 应用类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class WebApplication(BaseApplication):

    # 默认核心组件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def coreComponents(cls):
        return {
            'hrequest': {'clazz': 'hehe.core.web.WebRequest.WebRequest', '_scope': 'request'},
            'hresponse': {'clazz': 'hehe.core.web.WebResponse.WebResponse', '_scope': 'request'},
            'hrouter': {'clazz': 'hehe.core.hrouter.route.RouterManager'},
            'hvalidation': {'clazz': 'hehe.core.hvalidation.validation.Validation'},
            'hmiddleware': {'clazz': 'hehe.core.hmiddleware.middleware.MiddlewareManager'},
        }

    # 生成地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def toUrl(self, url = '', vars = {}, **options):

        uri = '';
        params = {};
        if isinstance(url, bool):
            uri = '/{0}'.format(he.app.route);
            params.update(he.app.hrequest.getQuery())
            params.update(vars)
        elif url == '':
            uri = '/{0}'.format(he.app.route);
            params.update(vars)
        else:
            # 分析url,使其支持模块或自动
            uri = url

        return self.routerRequest.buildUrl(uri, vars, **options)

