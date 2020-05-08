# -*- coding: utf-8 -*-
from hehe.helper.common import decorator
from hehe import he
import inspect

"""
 * 全局装饰器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""


# 缓存属性
# <B> 说明： </B>
# <pre>
# 略
# </pre
class cached_property(object):

    def __init__(self, func, name=None):

        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

        return ;

    def __get__(self, instance, cls=None):

        if instance is None:
            return self

        if self.name not in instance.__dict__.keys():
            res = instance.__dict__[self.name] = self.func(instance)
        else:
            res = instance.__dict__[self.name]

        return res

    def __set__(self, instance, val):

        instance.__dict__[self.name] = val

        return ;

# 缓存方法数据
# <B> 说明： </B>
# <pre>
# 略
# </pre
def hcache(**options):

    @decorator
    def generate(fn, *args, **kw):
        args = list(args)
        for key in list(kw.keys()):
            if not kw.get(key):
                kw.pop(key)

        self = None
        if args:
            self = args.pop(0)
        else:
            self = None

        opts = options.copy();
        cacheKey = opts.get('key',None);

        if cacheKey is None:
            raise Exception("cache key not find!")

        opts.pop('key');
        storageType = opts.get('storageType',None)
        cacheStorage = he.app.hcache.getStorage(storageType)

        if cacheStorage.exists(cacheKey):
            return cacheStorage.get(cacheKey)

        # 缓存结果
        result = fn(self, *args, **kw)
        cacheStorage.set(cacheKey,result,**opts);

        return result

    return generate

# 标识类为bean
# <B> 说明： </B>
# <pre>
# 略
# </pre
def hbean(beanId = '',**definition):

    def decorator(beanClazz):

        from hehe.core.hcontainer.utils import CommonUtil;

        beanDefinition = CommonUtil.buildBeanDefinition(beanId, beanClazz, definition);
        he.getBeanManager().batchRegister(beanDefinition)

        return beanClazz


    return decorator


# 标识类属性为其他bean组件对象装饰器
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def href(beanId,**definition):

    def decorator(property):

        from hehe.core.hcontainer.utils import CommonUtil;

        beanDefinition = CommonUtil.buildRefDefinition(beanId, property, definition);
        he.getBeanManager().batchRegister(beanDefinition)

        return property

    return decorator


def add_aop_aspect(func,behaviors,advice,pointcut = ''):

    beanManager = he.getBeanManager()

    from hehe.core.hcontainer.base.Definition import Definition;
    from hehe.core.hcontainer.base.aop import AopProxyHandler;

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

# 切面around(执行之前,执行之后)
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def haop_around(behaviors = [],pointcut = ''):

    def decorator(func):

        from hehe.core.hcontainer.base.aop import Aspect;
        add_aop_aspect(func,behaviors,Aspect.ADVICE_AROUND,pointcut)

        return func;

    return decorator

# 切面before(执行之后)
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def haop_before(behaviors=[], pointcut=''):

    def decorator(func):

        from hehe.core.hcontainer.base.aop import Aspect;
        add_aop_aspect(func, behaviors, Aspect.ADVICE_BEFORE, pointcut)

        return func;

    return decorator

# 切面after(执行之后)
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def haop_after(behaviors=[], pointcut=''):

    def decorator(func):

        from hehe.core.hcontainer.base.aop import Aspect;
        add_aop_aspect(func, behaviors, Aspect.ADVICE_AFTER, pointcut)

        return func;

    return decorator

# 切面afterThrowing(抛出异常之后)
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def haop_afterThrowing(behaviors=[], pointcut=''):

    def decorator(func):

        from hehe.core.hcontainer.base.aop import Aspect;
        add_aop_aspect(func, behaviors, Aspect.ADVICE_AFTERTHROWING, pointcut)

        return func;

    return decorator

# 切面afterReturning(执行并返回结果之后)
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def haop_afterReturning(behaviors=[], pointcut=''):

    def decorator(func):

        from hehe.core.hcontainer.base.aop import Aspect;
        add_aop_aspect(func, behaviors, Aspect.ADVICE_AFTERRETURNING, pointcut)

        return func;

    return decorator



# 注册路由规则
# <B> 说明： </B>
# <pre>
# 以类名为key
# </pre>
def hrouter_rule(uri = '',**ruleConf):

    def decorator(func):

        from hehe.core.hrouter import route
        rule = route.build_route_rule(uri,func,**ruleConf);
        he.app.hrouter.regRule(rule);

        return func

    return decorator

# 注册事件行为
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def hevent_behavior(eventName):

    def decorator(behavior):

        he.app.hevent.bindBehaviors(eventName, behavior)

        return behavior

    return decorator

# 注册中间件行为
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def hmiddleware_behavior(position):

    def decorator(behavior):

        he.app.hmiddleware.register(behavior,position)

        return behavior

    return decorator

# 注册验证器
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def hreg_validator(message = '',alias = ''):

    def decorator(validator):
        name = alias;
        if not name:
            name = validator.__name__

        he.app.hvalidation.registerValidator(name, validator,message)

        return validator

    return decorator

# 注册验证器规则
# <B> 说明： </B>
# <pre>
# 略
# </pre>
def hreg_valid_rule(validator,**ruleConf):

    def decorator(property):

        clazzModule = inspect.getmodule(property).__name__
        clazz = clazzModule + '.' + property.__qualname__.split('.')[0];
        propertyName = property.__name__;
        validatorAttr = {}
        if ruleConf:
            propertyName = ruleConf.get('property',propertyName);
            validatorAttr = ruleConf.get('attrs', {});

        he.app.hvalidation.regValidRule(clazz, propertyName,[validator,validatorAttr])

        return property

    return decorator









