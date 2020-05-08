# -*- coding: utf-8 -*-
"""
 *框架流程控制类
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
from hehe import he
from .Response import Response;
from .Request import Request;
from .Config import Config
from hehe.helper.ClassHelper import ClassHelper
from .exception import AppstopException

class BaseApplication:
    '''
        :type containerManager: hehe.core.hcontainer.beam.BeanManager
        :type conf: hehe.core.base.Config.Config
    '''


    # 构造方法
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param config 应用配置信息

    def __init__(self,config = Config):

        # 模块id
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.moduleId = None

        # 控制器id
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.controllerId = None

        # action id
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.actionId = None

        # 当前路由请求
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.routerRequest = None;

        # 当前路由
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.route = "index/index"

        # hrouter 路由对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.router = None;

        self.container = he.beanManager.makeContainer('request')

        self.read_static_res_status = False;

        he.app = self

        self.preInit(config)

        return ;


    # 应用业务入口
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def runApp(self):

        response = self.getRespone()
        try:
            # 初始化应用
            self.initApp()
            # 执行应用流程
            self.execApp()

        except AppstopException as e:
            pass;
        except Exception as e:
            raise e;
            if he.app.conf.onLog:
                he.exception(str(e));
            response.setContent(str(e))
        finally:
            he.triggerMiddleware("response_send_before")
            response.send()
            he.triggerMiddleware("response_send_after")
            # 应用结束
            self.endApp()

        return response;


    # 初始化之前
    # <B> 说明： </B>
    # <pre>
    # 一般处理配置信息
    # </pre
    def preInit(self,config = Config):

        self.conf = config;

        return ;


    # 初始化应用
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def initApp(self):

        he.triggerMiddleware("app_init")

        return ;

    # 执行app 流程
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def execApp(self):

        # 路由
        he.triggerMiddleware("app_exec")

        # 定位路由
        self.dispatch();
        # 执行控制器
        self.runAction();

        return ;

    # 应用结束
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def endApp(self):

        he.triggerMiddleware("app_end")

        return ;

    # 创建控制器对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    # :rurn BaseController
    def _getController(self):

        routeUrl = self.routerRequest.getRouteUrl()
        routeList = routeUrl.split('/')
        controllerId = routeList.pop(0);

        if self.conf.modules:
            module = self.conf.modules.get(controllerId, '')
            if module:
                self.moduleId = controllerId;
                self.controllerId = routeList.pop(0);

            self.actionId = routeList.pop(0);
        else:
            self.controllerId = controllerId;
            self.actionId = routeList.pop(0);

        controllerName = ClassHelper.ucfirst(self.controllerId) + he.app.conf.controllerSuffix;
        if self.moduleId:
            controllerNamespace = self.conf.modules.get(self.moduleId)
            controllerPackageName = controllerNamespace + '.' + controllerName + '.' + controllerName
        else:
            controllerPackageName = he.app.conf.controllerNamespace + '.' + controllerName + '.' + controllerName

        controller = he.makeBean(controllerPackageName);
        actionId = self.actionId;

        # 验证actions 字典
        if hasattr(controller, 'actions'):
            actions = controller.actions()
            if actions :
                controllerClass = actions.get(self.actionId,None);
                if controllerClass:
                    controller = he.makeBean(controllerClass);
                    actionId = 'run'

        # 初始化方法
        if hasattr(controller, '_init'):
            controller._init()

        return controller,self.buildActionName(actionId);

    # 构建action 名称
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def buildActionName(self,actionId):

        if not actionId or actionId == 'run':
            return 'run'

        return actionId + self.conf.actionSuffix;

    # 执行控制器方法
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def runAction(self):

        controller,actionName = self._getController();

        # 校验方法是否存在
        if not hasattr(controller,actionName):
            raise RuntimeError('controller action is not public or not exist')

        # 前置方法
        if hasattr(controller,'before_action'):
            beforeActionResult = controller.before_action()
            if beforeActionResult is False:
                return

        actionMeta = getattr(controller, actionName)

        # 触发中间件action 之前
        he.triggerMiddleware("action_before")

        content = actionMeta();
        if (isinstance(content,Response)):
            pass
        else:
            response = self.getRespone()
            response.setContent(content)

        # 后置方法
        if hasattr(controller,'after_action'):
            controller.after_action()

        # 触发中间件action 之后
        he.triggerMiddleware("action_after")

        return ;



    # 路由定位
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def dispatch(self):

        result = True;
        request = self.getRequest()

        # 定位路由
        self.routerRequest = self.getBean('hrouter').parseRequest(request.getEnviron());
        he.triggerMiddleware("dispatch_after")

        routeUrl = self.routerRequest.getRouteUrl()

        routeList = routeUrl.split('/')
        self.controllerId = routeList.pop(0);
        self.actionId = routeList.pop(0);

        return result;


    def getRespone(self):
        """
        :rtype:hehe.core.base.Response.Response|hehe.core.web.WebResponse.WebResponse
        :return:
        """

        return self.getBean('hresponse')

    def getRequest(self)->Request:
        """
        :rtype:hehe.core.base.Request.Request|hehe.core.web.WebRequest.WebRequest
        :return:
        """
        return self.getBean('hrequest')

    def initReqeust(self,environ):
        """
        :rtype:hehe.core.base.Request.Request
        :param environ:
        :return:
        """
        return self.getBean('hrequest').initEnviron(environ)


    # 默认核心组件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def coreComponents(cls):

        return {
            'hrequest': {'clazz': 'hehe.core.base.Request.Request','_scope':'request'},
            'hresponse': {'clazz': 'hehe.core.base.Response.Response','_scope':'request'},
            'hrouter': {'clazz': 'hehe.core.hrouter.route.RouterManager'},
            'hvalidation': {'clazz': 'hehe.core.hvalidation.validation.Validation'},
            'hevent': {'clazz': 'hehe.core.hevent.EventManager.EventManager'},
        }



    # 获取bean 对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getBean(self,beanId,*args,**kwargs):

        return he.getBean(beanId,*args,**kwargs);

    # 创建新对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def makeBean(self, beanId, *args, **kwargs):

        return he.makeBean(beanId, *args, **kwargs);

    # 生成地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def toUrl(self,uri = '',vars = {},**options):

        return self.routerRequest.buildUrl(uri,vars,**options)

    def getContainer(self):

        return self.container

    def __getattr__(self, name):

        return he.getBean(name)

    # 应用启动入口
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def run(cls, appConfig,**options):

        appConfig.appClass = cls;

        he.run(appConfig,**options)

        return ;



