# -*- coding: utf-8 -*-

from hehe.helper.ClassHelper import ClassHelper
from hehe import he;
"""
 * 服务接口类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
"""
class ServerManager:

    @classmethod
    def run(cls,config = None):
        """
        :param config:
        :type config:hehe.core.base.Config.Config

        """
        serverName = config.startup
        if not serverName:
            serverName = 'uwsgi';

        if serverName.find('.') == -1:
            serverClazz = __package__ + '.' + serverName + '.' + ClassHelper.ucfirst(serverName) + 'Server'
        else:
            serverClazz = serverName;

        serverMeta = ClassHelper.getClassMeta(serverClazz)
        startupServer = serverMeta(config);

        return startupServer.run();


"""
 * 服务接口类
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

class BaseServer:

    def __init__(self, config):

        self.config = config

        return;

    def run(self):

        return;




