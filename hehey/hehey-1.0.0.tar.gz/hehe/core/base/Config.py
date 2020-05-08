# -*- coding: utf-8 -*-


class Config:


    # 启动应用服务
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    startup = 'wsgiref';
    #startup = 'uwsgi';

    # 本地端口
    # <B> 说明： </B>
    # <pre>
    # 用于本地调试
    # </pre>
    localport = 8000;

    # 应用类
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    appClass = None

    # 应用id
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    appId = None

    # 应用基础目录
    # <B> 说明： </B>
    # <pre>
    # 应用根目录,如/home/hehe/www/apps/admin
    # </pre>
    appBasePath = ''

    # 应用静态资源目录
    # <B> 说明： </B>
    # <pre>
    # 应用静态资源目录,如/home/hehe/www/apps/admin/assets
    # </pre>
    staticPath = ''

    # 控制器名称后缀
    # <B> 说明： </B>
    # <pre>
    # class XxxxxController(HomeController):
    #   pass
    # </pre>
    controllerSuffix = 'Controller'

    # action 后缀
    # <B> 说明： </B>
    # <pre>
    # def xxxAction(self):
    #   pass
    # </pre>
    actionSuffix = 'Action'

    # 控制器包名
    # <B> 说明： </B>
    # <pre>
    # 如:admin.controllers
    # </pre>
    controllerNamespace = ''

    # 启用日志打印
    # <B> 说明： </B>
    # <pre>
    # 系统发生异常或错误,系统自动记录日志
    # </pre>
    onLog = False;

    # 启用session 会话
    # <B> 说明： </B>
    # <pre>
    # 启用会话后,应用自动调用session 中间件
    # </pre>
    onSession = False;

    # 引导模块
    # <B> 说明： </B>
    # <pre>
    # 主要为了加载模块,以及加载注解装饰器
    # ['site.behaviors.AddLog']
    # </pre>
    bootstrap = [];

    # 模块定义
    # <B> 说明： </B>
    # <pre>
    # {
    #   'site':"modules.site.controllers",
    #   'admin':"modules.admin.controllers"
    # }
    # </pre>
    modules = {};

    # 中间件
    # <B> 说明： </B>
    # <pre>
    # {
    #   'server_start':["modules.site.controllers"],
    #   'app_init':["modules.admin.controllers"]
    #   'app_exec':["modules.admin.controllers"]
    # }
    # </pre>
    middlewares = {
        # 服务启动
        'server_start':[],
        # 应用初始化
        'app_init':[
            'hehe.core.hmiddleware.middlewares.session.Session@open'
        ],
        # 路由之后
        'dispatch_after': [
            'hehe.core.hmiddleware.middlewares.LoadStaticRes.LoadStaticRes'
        ],
        # action 之前
        'action_before': [],
        # view 输出之前
        'view_output_before': [],
        # action 之后
        'action_after': [],
        # response 输出之前
        'response_send_before': [],
        # response 输出之后
        'response_send_after': [],
        # 应用发生异常
        'exception':[],
        # 应用结束
        'app_end': [
            #'hehe.core.hmiddleware.middlewares.session.Session@close'
        ]
    };


    #  应用组件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    components = {

    },

    params = {};

    #  设置属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setAttrs(self,attrs = {}):

        for attr in attrs:
            setattr(self, attr, attrs[attr])




