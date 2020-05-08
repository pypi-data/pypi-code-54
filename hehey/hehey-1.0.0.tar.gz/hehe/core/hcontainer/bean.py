# -*- coding: utf-8 -*-

from .base.Container import Container
from .base.Definition import Definition
from .utils import CommonUtil
from .base.aop import AopManager;
import inspect

# 创建容器管理器对象
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def make()->'BeanManager':

    return BeanManager.make()


"""
 * bean管理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class BeanManager():

    SCOPE_REQUEST = 'request';

    CLASS_KEY_NAME = "clazz";

    ID_KEY_NAME = "id";

    BEANMANAGER_KEY_NAME = "_beanManager";



    # 当前对象
    # <B> 说明： </B>
    # <pre>
    # app 应用级别,应用启动,开始生效
    # request 请求级别,每次请求时生效,请求结束后失效
    # </pre>
    manager = None;

    # 类bean定义
    # <B> 说明： </B>
    # <pre>
    # 通过类装饰器定义的bean 配置,以类路径为key
    # </pre>
    clazzBeanComponents = {}

    # 构造器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def __init__(self,components = {}):
        """ 定义属性　"""

        # 容器列表
        # <B> 说明： </B>
        # <pre>
        # app 应用级别,应用启动,开始生效
        # request 请求级别,每次请求时生效,请求结束后失效
        # </pre>
        self.scopeContainer = {}

        # bean定义对象列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.definitions = {}

        # bean 组件配置
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.components = components

        # 类与bend id 的对应关系
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.clazzBeanIdMap = {}

        # 初始化参数
        BeanManager.manager = self;

        # 注册组件
        self.batchRegister(self.formatBeanComponent())

        # 范围容器事件
        self.scopeEvent = {};


        self.aopManager = AopManager();

    @classmethod
    def getBeanManager(cls)->'BeanManager':

        return cls.manager

    def getAopManager(self)->'AopManager':

        return self.aopManager

    # 创建容器管理对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def make(cls,components = {})->'BeanManager':

        return cls(components);

    def setScopeEvent(self,**scopeEvent):

        self.scopeEvent = scopeEvent;

        return ;

    # 创建容器管理对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def makeContainer(self,scope):

        return Container(scope);

    # 获取指定应用对应的容器对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param scope 应用级别
    def getScopeContainer(self,scope)->'Container':

        scopeContainerFunc = self.scopeEvent.get(scope,None)
        if scopeContainerFunc is None:
            container = self.scopeContainer.get(scope,None);
            if container is None:
                container = Container(scope);
                self.scopeContainer[scope] = container
        else:
            container = scopeContainerFunc();

        return container

    # 清理容器
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def cleanScopeContainer(self,scopes = []):

        if scopes.count() == 0 :
            scopes.append(self.SCOPE_REQUEST)

        for scope in scopes:
            self.scopeContainer.pop(scope)

        return ;


    # 获取bean 实例
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param args 对象参数
    def getBean(self,beanId,*args ,**kwargs):

        definition = self.getDefinition(beanId)
        container = definition.getContainer()

        bean = None
        if container.hasBean(beanId) :
            bean = container.getBean(beanId)
        else:
            bean = definition.makeBean([args,kwargs])
            if definition.isSingle():
                container.setBean(beanId,bean)

        return bean

    # 是否定义bean
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param args 对象参数
    def hasComponent(self, beanId):

        component = self.components.get(beanId, None)
        if component is not None:
            return True
        else:
            return False

    # 创建一个新的bean对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param args 对象参数
    def makeBean(self, beanId, *args ,**kwargs):

        definition = self.getDefinition(beanId)
        bean = definition.make([args,kwargs])

        return bean

    # 获取bean 定义对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    def getDefinition(self,beanId)->Definition:

        definition = self.definitions.get(beanId,None)
        if definition:
            return definition;

        component = self.components.get(beanId,None)
        if component is None:
            component = {self.CLASS_KEY_NAME: beanId}

        component[self.ID_KEY_NAME] = beanId;

        # 在创建Definition　之前,先加载类的模块,以便让装饰器先执行
        className = component.get(self.CLASS_KEY_NAME,None)
        CommonUtil.getModuleMeta(className);

        mycomponent = self.components.get(beanId, None)
        if mycomponent:
            component = mycomponent;

        component[self.BEANMANAGER_KEY_NAME] = self;
        definition = Definition(**component)
        self.definitions[beanId] = definition

        return self.definitions[beanId]

    # 批量注册bean组件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    def batchRegister(self,components = {}):

        self.components.update(components)

        self.refreshClazzBeanIdMap();

        return ;

    def refreshClazzBeanIdMap(self):

        for beanId,component in self.components.items():
            self.clazzBeanIdMap[component[self.CLASS_KEY_NAME]] = beanId

        return ;

    def getBeanId(self,clazzName):

        beanId = self.clazzBeanIdMap.get(clazzName,None)

        if beanId is None:
            return clazzName
        else:
            return beanId

    # 追加配置
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    # :param component bean 配置信息
    def appendComponent(self,beanId, component):

        beanComponent = self.components.get(beanId,{})
        beanComponent.update(component)
        self.components[beanId] = beanComponent;
        self.refreshClazzBeanIdMap();

        return ;

    # 获取组件配置
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param beanId bean id
    def getComponents(self):

        return self.components

    # 注册装饰器bean 配置定义
    # <B> 说明： </B>
    # <pre>
    # 注入的属性自动叠加
    # </pre>
    @classmethod
    def registerBeanComponent(cls,beanDefinition):

        clazz = beanDefinition.get(cls.CLASS_KEY_NAME)

        beanComponent = cls.clazzBeanComponents.get(clazz,None)
        if beanComponent is None:
            beanComponent = beanDefinition
        else:
            beanComponent.update(beanDefinition)

        cls.clazzBeanComponents[clazz] = beanComponent;

        if cls.manager is not None:
            component = cls.formatComponentForBean(clazz,beanComponent)
            cls.manager.batchRegister(component);

        return ;


    @classmethod
    def formatComponentForBean(self,clazz,beanComponent):

        beanId = beanComponent.get(self.ID_KEY_NAME, None)
        if not beanId:
            beanId = clazz
        else:
            beanComponent[self.ID_KEY_NAME] = beanId;

        component = {};
        component[beanId] = beanComponent

        return component;

    @classmethod
    def formatBeanComponent(cls):

        componentList = {};
        for clazz in cls.clazzBeanComponents:
            beanComponent =  cls.clazzBeanComponents[clazz]
            beanId = beanComponent.pop(cls.ID_KEY_NAME,None)
            if not beanId:
                beanId = clazz
            else:
                beanComponent[cls.ID_KEY_NAME] = beanId;

            componentList[beanId] = beanComponent

        return componentList
