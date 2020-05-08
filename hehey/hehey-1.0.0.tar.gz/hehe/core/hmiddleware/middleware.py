from .utils import CommonUtil
from inspect import isfunction
from hehe import he
"""
 * 中间件管理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class MiddlewareManager(object):

    def __init__(self,**attrs):

        self.middlewares = {};

        if attrs:
            CommonUtil.setAttrs(self,attrs)

        return ;


    """
     * 设置中间件
     *<B>说明：</B>
     *<pre>
     *  覆盖中间件
     *</pre>
    """
    def setMiddlewares(self,middlewares):

        self.middlewares.update(middlewares)

        return ;

    """
     * 注册追加中间件
     *<B>说明：</B>
     *<pre>
     *  略
     *</pre>
    """
    def register(self,middlewares,position):

        middlewareList = self.middlewares.get(position,[])
        middlewareList = middlewareList + middlewares
        self.middlewares[position] = middlewareList

        return ;

    """
     * 触发中间件
     *<B>说明：</B>
     *<pre>
     *  略
     *</pre>
    """
    def trigger(self,position,*args ,**kwargs):

        middlewareList = self.middlewares.get(position, [])
        if not middlewareList:
            return ;

        result = False;
        for middleware in middlewareList:
            # 判断行为类型是方法,或类对象
            if isfunction(middleware):
                middlewareMethodMeta = middleware
            else:
                middlewareMethodMeta = self.buildMiddlewareMethodMeta(middleware)

            result = middlewareMethodMeta(*args ,**kwargs)

            if isinstance(result,bool):
                if result is True:
                    he.raiseAppstopException()
                else:
                    break;

        return result;


    def buildMiddlewareMethodMeta(self,middleware):

        middlewareName = middleware

        if middlewareName.find('@@') != -1:
            middlewareClass, methodName = middlewareName.split("@@")
            middlewareMeta = CommonUtil.getClassMeta(middlewareClass)
            middlewareMethodMeta = getattr(middlewareMeta, methodName)
        elif middlewareName.find('@') != -1:
            middlewareClass, methodName = middlewareName.split("@")
            middlewareMeta = CommonUtil.getClassMeta(middlewareClass)
            middlewareMethodMeta = getattr(middlewareMeta(), methodName)
        else:
            middlewareMeta = CommonUtil.getClassMeta(middlewareName)
            middlewareMethodMeta = getattr(middlewareMeta(), 'handle')


        return middlewareMethodMeta;