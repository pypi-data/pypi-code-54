# -*- coding: utf-8 -*-

"""
 * api 控制器
 *<B>说明：</B>
 *<pre>
 *  默认一个接口对应action 文件
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
import inspect

class ApiController(WebController):

    def actions(self):

        clazzModule = inspect.getmodule(self).__name__;
        actionName = ClassHelper.ucfirst(he.app.buildActionName(he.app.actionId))
        clazzName = '{0}.{1}.{2}.{3}'.format(ClassHelper.dirname(clazzModule),he.app.controllerId,actionName,actionName);

        return {he.app.actionId:clazzName};


