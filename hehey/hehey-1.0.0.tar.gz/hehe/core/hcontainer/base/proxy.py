
from types import FunctionType
from types import MethodType
import importlib

"""
 * 代理事件
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class ProxyHandler():


    def __init__(self,target:object = None):

        self.target = target;

        self.beanManager = None;

    def setBeanManager(self,beanManager):

        self.beanManager = beanManager;

        return ;

    def getBeanManager(self):

        return self.beanManager;

    def invoke(self,method,*args ,**kwargs):

        return self.target.__getattribute__(method)(*args ,**kwargs)

    def __getattr__(self, name):

        return getattr(self.target,name);

"""
 * bean代理类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
"""
class BeanProxy():

    @classmethod
    def make(cls,className,proxyHandler:ProxyHandler):
        proxyClassName = cls.buildProxyClassName(className);
        proxyClassCode = cls.buildProxyClass(proxyClassName);
        mydata = {};
        proxyClassMeta = None;
        mydata['proxyClassMeta'] = proxyClassMeta
        exec(proxyClassCode,mydata)
        return mydata['proxyClassMeta'](proxyHandler);

    @classmethod
    def buildProxyClass(cls,proxyClassName):

        # 代理类模板
        proxyClassTpl = '''
from types import FunctionType
from types import MethodType      
class {0}:

    def __init__(self, proxyHandler):

        self.proxyHandler = proxyHandler;

    def __getattr__(self, name):

        attrValue = getattr(self.proxyHandler,name)

        if isinstance(attrValue,MethodType) or isinstance(attrValue,FunctionType):
            def _func(*arg, **kwargs):
                return self.proxyHandler.invoke(_func.func_name,*arg, **kwargs)

            _func.func_name = name

            return _func;
        else:

            return attrValue
        
proxyClassMeta = {0}

        
        '''

        proxyClassTpl = proxyClassTpl.format(proxyClassName)


        return proxyClassTpl;

    @classmethod
    def buildProxyClassName(cls,className):

        name = className.replace('.','_')

        return '{0}_Proxy'.format(name)


# class ProxyClass():
#
#     def __init__(self, proxyHandler:ProxyHandler):
#
#         self.proxyHandler = proxyHandler;
#
#     def __getattr__(self, name):
#
#         attrValue = getattr(self.proxyHandler,name)
#
#         if isinstance(attrValue,MethodType) or isinstance(attrValue,FunctionType):
#             def _func(*arg, **kwargs):
#                 return self.proxyHandler.invoke(_func.func_name,*arg, **kwargs)
#
#             _func.func_name = name
#
#             return _func;
#         else:
#
#             return attrValue

