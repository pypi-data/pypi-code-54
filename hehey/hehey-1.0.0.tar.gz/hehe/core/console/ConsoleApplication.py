# -*- coding: utf-8 -*-
"""
 * 控制台应用类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
from hehe.core.base.BaseApplication import BaseApplication
class ConsoleApplication(BaseApplication):

    # 默认核心组件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def coreComponents(cls):
        return {
            'hrequest': {'clazz': 'hehe.core.console.ConsoleRequest.ConsoleRequest'},
            'hresponse': {'clazz': 'hehe.core.console.ConsoleResponse.ConsoleResponse'},
            'hrouter': {'clazz': 'hehe.core.hrouter.route.RouterManager'},
            'hvalidation': {'clazz': 'hehe.core.hvalidation.validation.Validation'},
            'hmiddleware': {'clazz': 'hehe.core.hmiddleware.middleware.MiddlewareManager'},
        }


