

"""
无效参数异常
"""
class InvalidParamException(Exception):

    pass;

"""
路由定位异常
"""
class InvalidRouteException(Exception):

    pass;

"""
程序中断
"""
class AppstopException(Exception):

    pass;

"""
页面未找到异常
"""
class NotFoundException(Exception):

    pass;

"""
业务异常
"""
class ServiceException(Exception):

    pass;