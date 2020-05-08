
from .proxy import ProxyHandler;
from ..utils import CommonUtil
import re;

"""
 * aop 切面类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class Aspect():

    ADVICE_BEFORE = 'before';
    ADVICE_AROUND = 'around';
    ADVICE_AFTER = 'after';
    ADVICE_AFTERTHROWING = 'afterThrowing';
    ADVICE_AFTERRETURNING = 'afterReturning';

    def __init__(self,pointcut = ''):

        # 通知点行为
        # <B> 说明： </B>
        # <pre>
        # 基本格式:['通知点位置'=>'行为列表',]
        # </pre>
        self.advices = {};

        # 拦截点
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.pointcut = pointcut;


    def setPointcut(self,pointcut):

        self.pointcut = pointcut;

        return ;

    def getMatch(self):

        if hasattr(self,'_matchPointcut'):
            return getattr(self,'_matchPointcut')

        # 如果首尾字符/,表示正则表达式
        if self.pointcut[0] == '/' and self.pointcut[-1] == '/':
            matchPointcut = self.pointcut[1:-1];
            setattr(self,'_matchPointcut',matchPointcut)
            return self.pointcut[1:-1];

        # 替换星号
        matchPointcut = self.pointcut.replace('*','(\w+)')
        setattr(self, '_matchPointcut', matchPointcut)
        return matchPointcut;


    def addBehavior(self,advice,behaviors = []):

        if isinstance(behaviors,str):
            behaviorList = behaviors.split(',')
        else:
            behaviorList = behaviors.copy();

        behaviors = self.advices.get(advice,[])
        behaviors = behaviors + behaviorList
        self.advices[advice] = behaviors;

        return ;


    def hasAdvice(self,advice):

        if self.advices.get(advice, None) is None:
            return False
        else:
            return True


    def getAdviceBehaviors(self,advice):

        return self.advices.get(advice,None);

    # 执行通知行为
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def doAdvice(self,target,method, *args ,**kwargs):

        doResult = None;
        parameters = {
            'args': args,
            'kwargs': kwargs
        };

        doException = None;

        try:
            methodMeta = getattr(target, method)
            # 环绕通知
            if self.hasAdvice(self.ADVICE_AROUND):
                self.doBehaviors(self.ADVICE_AROUND,target,method, parameters,doResult,doException)
                doResult =  methodMeta(*args ,**kwargs)
                self.doBehaviors(self.ADVICE_AROUND, target, method, parameters,doResult,doException)
            else:
                # 前置通知
                if self.hasAdvice(self.ADVICE_BEFORE):
                    self.doBehaviors(self.ADVICE_BEFORE, target, method, parameters,doResult,doException)
                doResult = methodMeta(*args, **kwargs)

                if self.hasAdvice(self.ADVICE_AFTER):
                    self.doBehaviors(self.ADVICE_AFTER, target, method, parameters,doResult,doException)

        except Exception as e:
            if self.hasAdvice(self.ADVICE_AFTERTHROWING):
                self.doBehaviors(self.ADVICE_AFTERTHROWING, target, method, parameters,doResult,doException)

            raise e;

        if self.hasAdvice(self.ADVICE_AFTERRETURNING):
            self.doBehaviors(self.ADVICE_AFTERRETURNING, target, method, parameters,doResult,doException)

        return doResult;

    # 执行通知点行为
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def doBehaviors(self,advice,target,method, parameters,doResult,doException):

        behaviorList = self.getAdviceBehaviors(advice)
        if not behaviorList:
            return ;

        for behavior in behaviorList:
            if isinstance(behavior,str):
                behaviorMeta = CommonUtil.getModuleMeta(behavior)
                behavior = behaviorMeta();
            else:
                if isinstance(behavior,type):
                    behaviorMeta = behavior;
                    behavior = behaviorMeta();
                else:
                    # 对象
                    pass

            behavior.invoke(target,method,parameters,doResult,doException);

        return ;

"""
 * aop 代理处理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class AopProxyHandler(ProxyHandler):

    def invoke(self,method,*args ,**kwargs):

        aopManager =  self.getBeanManager().getAopManager();

        return aopManager.execute(self.target,method,*args ,**kwargs);

"""
 * aop 行为类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class AopBehavior():

    def __init__(self,**attrs):

        if attrs:
            CommonUtil.setAttrs(self,attrs)


    def invoke(self,target,method,parameters,doResult,doException):

        return ;

"""
 * aop 管理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class AopManager():

    def __init__(self):

        self.aspects = {}

    # 执行通知点行为
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def addAspect(self,aopBehaviors = [],advice = None,pointcut = None):

        aspect = self.aspects.get(pointcut,None);
        if aspect is None:
            aspect = Aspect(pointcut);

        aspect.addBehavior(advice,aopBehaviors)

        self.aspects[pointcut] = aspect

        return ;

    def appendAspect(self,pointcut,aspect):

        self.aspects[pointcut] = aspect


    def matchAspect(self,exp)->'Aspect':

        aspect = self.aspects.get(exp,None);
        if aspect is not None:
            return aspect


        matchAspect = False;
        # 正则匹配
        for pattern,aspect in self.aspects.items():
            matchReg = aspect.getMatch();
            if re.match(matchReg, exp):
                matchAspect = aspect;

        return matchAspect;


    def buildPointcutExp(self,clazz,method):

        clazzName = CommonUtil.getClassName(clazz)

        return '{0}.{1}'.format(clazzName,method);

    def execute(self,target,method,*args ,**kwargs):

        exp = self.buildPointcutExp(target,method)
        aspect = self.matchAspect(exp);

        # 未找到拦截点,直接执行目标方法
        if aspect is False:
            methodMeta = getattr(target, method)
            return methodMeta(*args ,**kwargs);
        else:

            return aspect.doAdvice(target,method,*args ,**kwargs)
