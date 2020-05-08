from ..bean import BeanManager
from .Definition import Definition
from .aop import AopProxyHandler
from .aop import Aspect
import inspect

from hehe.core.hcontainer.utils import CommonUtil

# 标识类为bean组件装饰器
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def id(beanId = '',**definition):

    def decorator(beanClazz):

        beanDefinition = CommonUtil.buildBeanDefinition(beanId,beanClazz,definition);
        BeanManager.registerBeanComponent(beanDefinition)

        return beanClazz

    return decorator

# 标识类属性为其他bean组件对象装饰器
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def ref(beanId,**definition):

    def decorator(property):

        beanDefinition = CommonUtil.buildRefDefinition(beanId, property, definition);
        BeanManager.registerBeanComponent(beanDefinition)

        return property

    return decorator

def add_aspect(func,behaviors,advice,pointcut = ''):

    beanManager = BeanManager.getBeanManager();
    aopManager = beanManager.getAopManager()
    clazzModule = inspect.getmodule(func).__name__
    className = clazzModule + '.' + func.__qualname__.split('.')[0];

    if not pointcut:
        aspectPointcut = className + '.' + func.__name__;
    else:
        aspectPointcut = pointcut;

    beanId = beanManager.getBeanId(className);
    aopManager.addAspect(behaviors, advice, aspectPointcut)
    component = {
        Definition.SYS_ATTR_ONPROXY: True,
        Definition.SYS_ATTR_PROXYHANDLER: AopProxyHandler,
        Definition.SYS_ATTR_CLASS: className
    };

    beanManager.appendComponent(beanId, component)

    return ;

def Around(behaviors = [],pointcut = ''):

    def decorator(func):

        add_aspect(func,behaviors,Aspect.ADVICE_AROUND,pointcut)

        return func;

    return decorator


def Before(behaviors=[], pointcut=''):
    def decorator(func):
        add_aspect(func, behaviors, Aspect.ADVICE_BEFORE, pointcut)

        return func;

    return decorator

def After(behaviors=[], pointcut=''):
    def decorator(func):
        add_aspect(func, behaviors, Aspect.ADVICE_AFTER, pointcut)

        return func;

    return decorator

def AfterThrowing(behaviors=[], pointcut=''):
    def decorator(func):
        add_aspect(func, behaviors, Aspect.ADVICE_AFTERTHROWING, pointcut)

        return func;

    return decorator

def AfterReturning(behaviors=[], pointcut=''):
    def decorator(func):
        add_aspect(func, behaviors, Aspect.ADVICE_AFTERRETURNING, pointcut)

        return func;

    return decorator





