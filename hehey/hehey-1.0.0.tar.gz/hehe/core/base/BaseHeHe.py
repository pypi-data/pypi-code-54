# -*- coding: utf-8 -*-

"""
 * 应用全局控制类
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

from hehe.core.base.Config import Config

import logging
import threading
import importlib

class BaseHeHe:

    '''
    :type app: hehe.core.base.BaseApplication.BaseApplication|common.Component.Component|hehe.core.base.Component.Component
    :type beanManager: hehe.core.hcontainer.bean.BeanManager
    :type application: hehe.core.web.WebApplication.WebApplication
    :type config: hehe.core.base.Config.Config

    '''



    def __init__(self):

        self._app = {};

        # 容器管理器
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.beanManager = None

        # app 应用类
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.application = None

        # 启动状态
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.startup = False;

        # 配置基础
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.config = None

        # 生成容器
        from hehe.core.hcontainer.bean import BeanManager
        if self.beanManager is None:
            self.beanManager = BeanManager.make()
            self.beanManager.setScopeEvent(request=self.__getRequestContainer)


        return ;

    # 获取bean 对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getBean(self,beanId,*args,**kwargs):

        return self.beanManager.getBean(beanId,*args,**kwargs)

    # 创建新对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def makeBean(self, beanId, *args ,**kwargs):

        return self.beanManager.makeBean(beanId,*args,**kwargs)

    # 获取bean 对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def hasComponent(self, beanId):

        return self.beanManager.hasComponent(beanId)

    def getBeanManager(self):
        '''
        :rtype:hehe.core.hcontainer.bean.BeanManager

        '''
        return self.beanManager

    @property
    def app(self):

        """
        :rtype:hehe.core.base.BaseApplication.BaseApplication|common.Component.Component|hehe.core.base.Component.Component
        :return:
        """

        app = self._app.get(id(threading.current_thread()),None);
        if app is None:
            return self._app.get(id(threading.main_thread()), None);

        return app

    @app.setter
    def app(self,value):

        self._app[id(threading.current_thread())] = value

        return ;

    # 初始化操作
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def _init(self):

        self._app = {};

        # 组件bean注入容器
        appComponents = {}
        appComponents.update(self.config.appClass.coreComponents())
        appComponents.update(self.config.components)
        self.beanManager.batchRegister(appComponents)

        # 加载引导模块
        if self.config.bootstrap:
            for module in self.config.bootstrap:
                importlib.import_module(module)

        # 注册中间件
        hmiddleware = self.getBean('hmiddleware')
        hmiddleware.setMiddlewares(self.config.middlewares)

        self.triggerMiddleware("server_start")

        return ;

    # 应用启动入口
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def run(self, appConfig,**options):

        """
        :param config:
        :type config:hehe.core.base.Config.Config

        """
        if self.startup:

            return ;

        self.startup = True;
        from hehe.server.server import ServerManager

        if isinstance(appConfig,type):
            self.config = appConfig()
        else:
            self.config = appConfig

        # 合并参数
        self.config.setAttrs(options)

        self._init()

        return ServerManager.run(self.config)


    # 获取请求的bean容器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def __getRequestContainer(self):

        return self.app.getContainer()

    def getRequest(self):

        return self.app.getRequest();

    def getRespone(self):

        return self.app.getRespone();

    # 触发中间件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def triggerMiddleware(self,position,*args ,**kwargs):

        hmiddleware = self.getBean('hmiddleware')

        return hmiddleware.trigger(position,*args ,**kwargs);

    # 注册中间件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def registerMiddleware(self,position, middlewares):

        hmiddleware = self.getBean('hmiddleware')

        return hmiddleware.register(position, middlewares);

    # 获取语言包
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def lang(self,name,params = {},app = '',packageName = None,lang = None):

        if name.find(':') == -1:
            if not app:
                app = self.app.conf.appId
            key = '{0}:{1}'.format(app,name)
        else:
            key = name;

        return self.app.hi18n.getMessage(key,params,packageName,lang);


    def log(self,level,msg,loggerName = '', *args, **kwargs):

        # 添加请求id
        extra = kwargs.get("extra",{})
        extra['reqid'] = self.app.hrequest.getRequestId();
        kwargs['extra'] = extra

        return self.app.hlog.log(level,msg,loggerName,*args, **kwargs);

    def raiseAppstopException(self):

        from .exception import AppstopException

        raise AppstopException();

    # 打印日志debug
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def debug(self, msg,loggerName = '', *args, **kwargs):

        return self.log(logging.DEBUG,msg,loggerName,*args, **kwargs);

    # 打印日志info
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def info(self, msg, loggerName='', *args, **kwargs):

        return self.log(logging.INFO,msg,loggerName,*args, **kwargs);


    # 打印日志warning
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def warning(self, msg, loggerName='', *args, **kwargs):

        return self.log(logging.WARNING,msg,loggerName,*args, **kwargs);


    # 打印日志error
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def error(self, msg, loggerName='', *args, **kwargs):

        return self.log(logging.ERROR,msg,loggerName,*args, **kwargs);

    # 打印日志critical
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def critical(self, msg, loggerName='', *args, **kwargs):

        return self.log(logging.CRITICAL,msg,loggerName,*args, **kwargs);

    # 打印日志exception
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def exception(self, msg, loggerName='', *args, **kwargs):

        return self.log(logging.ERROR,msg,loggerName,*args, **kwargs);
