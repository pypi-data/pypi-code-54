
from .utils import CommonUtil;
from hehe import he

"""
 * 视图类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class View():

    def __init__(self,**attrs):


        # 当前模板引擎对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.engine = None;

        # 默认模板引擎类型
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.defaultEngine = 1;

        # 所有模板引擎对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.engines = {};

        # 定义的模板引擎
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.customEngines = {}

        if attrs:
            CommonUtil.setAttrs(self,attrs)

    # 创建模板引擎对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def makeEngine(self,engineType,options = {}):

        clazz = options.get('clazz',engineType)

        if not clazz:
            raise Exception('the view {0} engine conf no find clazz'.format(engineType))

        if clazz.find('.') == -1:
            clazzName = CommonUtil.ucfirst(clazz) + 'Engine'
            clazz = __package__ + '.' + clazzName + '.' + clazzName

        engineMeta = CommonUtil.getClassMeta(clazz)

        return engineMeta(**options);

    # 获取指定类型的模板引擎对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getEngine(self,engineType = '')->'Engine':

        if not engineType:
            engineType = self.defaultEngine;


        engine = self.engines.get(engineType,None)

        if engine:
            return engine

        engineConf = self.customEngines.get(engineType,None)
        if engineConf is None:
            raise Exception('the {0} engine conf no find'.format(engineType))

        engine = self.makeEngine(engineType,engineConf);
        self.engines[engineType] = engine

        return engine;

    # 设置视图数据
    # <B> 说明： </B>
    # <pre>
    # 使用默认模板引擎
    # </pre>
    def assign(self,name,value):

        engine = self.getEngine();
        engine.assign(name,value);

        return self;

    # 加载模板
    # <B> 说明： </B>
    # <pre>
    # 使用默认模板引擎
    # </pre>
    def fetch(self,template,data = {}):

        engine = self.getEngine();
        content = engine.fetch(template,data);

        he.triggerMiddleware("view_output_before",content)

        return content;

    def __getattr__(self, engineType):
        """
        :rtype:Engine
        :return:
        """
        return self.getEngine(engineType)


"""
 * 视图引擎基类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class Engine():

    def __init__(self, **config):

        # 模板配置
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.config = config;

        # 模板数据
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.data = {};


    def assign(self,name,value):

        self.data[name] = value;

        return self;

    def fetch(self,tpl ,data = {}):

        tpldata = {};
        if data:
            tpldata = data.copy()

        tpldata = dict(tpldata,**self.data);

        self.data = {};

        return self.fetchInternal(tpl,tpldata);

    def fetchInternal(self,tpl,data):

        return ;




