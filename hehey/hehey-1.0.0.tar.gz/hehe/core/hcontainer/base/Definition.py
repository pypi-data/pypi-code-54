# -*- coding: utf-8 -*-
from .Container import Container
from .ClassReflection import ClassReflection
import re
from ..utils import CommonUtil
from threading import Condition
from .proxy import BeanProxy

"""
 * bean 定义类描述
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class Definition():

    BEAN_REF_REGEX = r'<ref::([^>]+)?>'
    PARAMS_REGEX = r'<(.+)::([^>]+)?>'
    PARAMS_SPLIT_CHARACTER = '|';

    SYS_ATTR_ONPROXY = '_onProxy';
    SYS_ATTR_PROXYHANDLER = '_proxyHandler';
    SYS_ATTR_CLASS = 'clazz';

    # 系统默认属性
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    sysAttr = ['_attrs', '_scope', '_ref','_func', 'clazz', '_single', '_init', '_args', '_onProxy', '_proxyHandler','_beanManager'];

    def __init__(self,id = '' ,**attrs):

        # 容器全局唯一id
        # <B> 说明： </B>
        # <pre>
        # 如未设置,则默认为对象的类名
        # </pre>
        self._id = "";

        # 其他bean id
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._ref = None;

        # 方法
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._func = [];

        # 配置基础
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.clazz = None;

        # 构造方法参数，支持索引，关联数组
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._args = [];

        # 类其他属性，直接注入
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._attrs = [];

        # 是否生成代理对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._onProxy = False;

        # 代理类事件处理器
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._proxyHandler = None;

        # 作用范围
        # <B> 说明： </B>
        # <pre>
        # app 应用级别(每次请求结束后自动销毁)
        # forever 永久级别(必须重启php 服务后才能自动销毁)
        # </pre>
        self._scope = 'app';

        # 反射对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.reflection = None;

        # 初始化参数
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._init = None;

        # 是否单例
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._single = True

        self.__formatArgs = None

        self.__formatAttrs = None
        self._id = id;

        self.lock = Condition()

        self._beanManager = None;

        if attrs:
            befinitionAttrs = self.formatAttributes(attrs);
            CommonUtil.setAttrs(self, befinitionAttrs)

        return ;

    def getId(self):

        return self._id

    def getRef(self):

        return self._ref

    def getClazz(self):

        return self.clazz

    def setSingle(self,single = True):

        self._single = single

    def isSingle(self):

        return self._single

    def setBeanManager(self,beanManager):

        self._beanManager = beanManager;

        return ;


    def getContainer(self)->'Container':

        return self.getBeanManager().getScopeContainer(self._scope)

    def getBeanManager(self):

        if self._beanManager is None:
            from ..bean import BeanManager
            return BeanManager.getBeanManager();
        else:
            return self._beanManager


    def makeBean(self,args):

        container = self.getContainer()
        # 单例加锁
        if self.isSingle():
            self.lock.acquire();

        try:
            if self.isSingle() and container.hasBean(self._id):
                # 再此验证
                bean = container.getBean(self._id);
                return bean


            bean = self.make(args);
            if self.isSingle():
                container.setBean(self._id, bean)

            return bean;
        finally:
            if self.isSingle():
                self.lock.release();
        return;


    # 创建bean 对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def make(self,args):


        if self._ref is not None:

            return self.getBeanManager().getBean(self._ref)
        elif self._func:
            funcMeta =  self._func[0];
            funcParamstuple = self._func[1];
            return funcMeta(*funcParamstuple);
        else:
            # 获取反射类
            reflection = self.getReflection()
            # 构建器参数
            parameters = self.buildArgs(args);
            # 创建对象
            beanObj = reflection.make(parameters)

            # 设置属性
            if self._attrs :
                self.buildAttrs()
                CommonUtil.setAttrs(beanObj,self.__formatAttrs)

            # 调用初始化方法
            if self._init:
                initFuncMeta = getattr(beanObj,self._init)
                initFuncMeta()

            if self._onProxy is True:
                beanObj = self.makeProxyBean(beanObj);

            return beanObj

    # 创建代理类
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def makeProxyBean(self,bean):

        if not self._proxyHandler:

            return bean;

        if isinstance(self._proxyHandler,str):
            proxyHandlerMeta = CommonUtil.getModuleMeta(self._proxyHandler)
        else:
            proxyHandlerMeta = self._proxyHandler

        proxyHandler = proxyHandlerMeta(bean);
        proxyHandler.setBeanManager(self._beanManager)
        clazzName = CommonUtil.getClassName(bean)
        beanProxy = BeanProxy.make(clazzName,proxyHandler);
        return beanProxy;

    # 构建类的构造参数(args)
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildArgs(self,args):

        if self.__formatArgs is None:
            self.__formatArgs = self.formatArgs(self._args)

        beanArgs = []
        beanArgs = beanArgs + self.__formatArgs
        userArgs = args[0]
        if len(beanArgs) >= len(userArgs):
            if len(userArgs) == 1 and not userArgs[0]:
                pass
            else:
                for i in range(len(userArgs)):
                    beanArgs[i] = userArgs[i]

            args[0] = beanArgs;

        return args

    # 构建类属性(attrs)
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildAttrs(self):

        if self.__formatAttrs is None:
            self.__formatAttrs = self.formatAttrs(self._attrs)

        return ;

    # 获取反射对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getReflection(self):

        if self.reflection is None:
            self.reflection = ClassReflection(self.clazz)

        return self.reflection

    # 整理类自定义参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def formatAttributes(cls,attrs = {}):

        attributes = {}
        customAttrs = {}
        for attr in attrs:
            if attr in cls.sysAttr:
                attributes[attr] = attrs[attr]
            else:
                customAttrs[attr] = attrs[attr]

        _argsStatus = attributes.get('_args',None)
        if _argsStatus is True:
            attributes['_args'] = [customAttrs]
        else:
            attributes['_attrs'] = customAttrs

        return attributes

    # 构建参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def formatAttrs(cls,attrs = {}):

        if not attrs :
            return attrs

        newAttrs = {};
        for key in attrs:
            value = attrs[key]
            if key[0] == '@':
                newAttrs[key[1:]] = cls.formatBean(value,True)
            else:
                newAttrs[key] = cls.formatBean(value)

        return newAttrs

    @classmethod
    def formatArgs(cls,args = []):

        if not args :
            return args

        if isinstance(args,dict):
            return [args]

        for index in range(len(args)):
            args[index] = cls.formatBean(args[index])

        return args

    @classmethod
    def formatBean(cls,value,ergodic = False):

        if ergodic:
            if isinstance(value,dict):
                for key in value:
                    value[key] = cls.getBeanValue(value[key])
            elif isinstance(value,list):
                for index in range(len(value)):
                    value[index] = cls.getBeanValue(value[index])
        else:
            if type(value) == cls:
                value = value.make([])
            else:
                if type(value) == str:
                    value = cls.getBeanValue(value)

        return value

    @classmethod
    def getBeanValue(cls, value):

        refMatch = re.match(cls.BEAN_REF_REGEX, value)
        if refMatch:
            ref = refMatch.group(1);
            definition = Definition(_ref = ref)
            value = definition.make([])
        else:
            funcMatch = re.match(cls.PARAMS_REGEX, value)
            if funcMatch:
                funcName = funcMatch.group(1);
                funcParams = funcMatch.group(2)
                funcMeta = CommonUtil.getModuleMeta(funcName)
                funcParamstuple = tuple(funcParams.split(cls.PARAMS_SPLIT_CHARACTER))

                definition = Definition(_func = [funcMeta, funcParamstuple])
                value = definition

        return value








