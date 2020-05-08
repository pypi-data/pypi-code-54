# -*- coding: utf-8 -*-
from .utils import CommonUtil
from .base.BaseEvent import BaseEvent
import copy
# 注册事件行为
# def reg_event_behavior(eventName):
#     def decorator(behavior):
#
#         EventManager.registerBehaviors(eventName,behavior)
#
#         return behavior
#
#     return decorator
#
# # 注册事件条件
# def reg_event_when(eventName):
#
#     def decorator(func):
#
#         currentModule = inspect.getmodule(func)
#         if currentModule.__name__ == '__main__':
#             when = func.__qualname__
#         else:
#             when = currentModule.__name__ + '.' + func.__name__
#
#         EventManager.registerWhen(eventName,when)
#
#         return func
#
#     return decorator

"""
 * 事件管理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class EventManager:


    def __init__(self,**attrs):

        # 自定义事件
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.customEvents = {};

        # 事件列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.events = {}

        if attrs:
            CommonUtil.setAttrs(self,attrs)

        return ;

    # 获取事件对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param eventName 事件名称
    # :param behavior 行为类路径
    def getEvent(self,eventName)->'Event':

        event = self.events.get(eventName, None)
        if event:
            return event;

        eventAttrs = self.customEvents.get(eventName,None);
        if not eventAttrs:
            eventAttrs = {"name":eventName};

        event = Event(**eventAttrs)

        self.events[eventName] = event;

        return event;


    # 绑定事件行为
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param eventName 事件名称
    # :param behavior 行为类
    def bindBehaviors(self,eventName,behavior):

        event = self.getEvent(eventName)
        event.addBehavior(behavior)

        return self;


    # 触发事件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # :param eventName 事件名称
    # :param data 触发数据
    def trigger(self,eventName,data = None):

        event = self.getEvent(eventName)
        if not event:
            return False;

        myevent = copy.copy(event)
        myevent.setData(data)

        return myevent.trigger()


class Event(BaseEvent):

    pass


