# -*- coding: utf-8 -*-
from ..utils import CommonUtil
from inspect import isfunction

"""
 * 事件基类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""

class BaseEvent:

    def __init__(self,**attrs):

        # 事件名称
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.name = ''

        # 事件行为
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.behaviors = []

        # 事件数据
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.data = {}

        if attrs:
            CommonUtil.setAttrs(self,attrs)

        return ;


    def getName(self):

        return self.name

    def setData(self,data):

        self.data = data

    def setBehaviors(self,behaviors = []):

        self.behaviors = behaviors;

        return ;

    # 添加事件行为
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param behavior 行为类路径
    # :param alias 行为类别名
    def addBehavior(self,behavior):

        self.behaviors.append(behavior)

        return ;


    # 触发当前事件
    # <B> 说明： </B>
    # <pre>
    # 触发行为操作
    # </pre>
    # :return boolean
    def trigger(self)->bool:

        result = False;
        for behaviorClazz in self.behaviors:
            # 判断行为类型是方法,或类对象
            if isfunction(behaviorClazz):
                result = behaviorClazz(self)
            else:
                if behaviorClazz.find('@@') != -1:
                    behaviorClazz, methodName = behaviorClazz.split("@@")
                    behaviorMeta = CommonUtil.getClassMeta(behaviorClazz)
                    methodMeta = getattr(behaviorMeta, methodName)
                elif behaviorClazz.find('@') != -1:
                    behaviorClazz, methodName = behaviorClazz.split("@")
                    behaviorMeta = CommonUtil.getClassMeta(behaviorClazz)
                    behavior = behaviorMeta();
                    methodMeta = getattr(behavior, methodName)

                else:
                    methodName = 'handle';
                    behaviorMeta = CommonUtil.getClassMeta(behaviorClazz)
                    behavior = behaviorMeta();
                    methodMeta = getattr(behavior, methodName)

                result = methodMeta(self)

            if isinstance(result,bool) and result is False:
                break;

        return result

