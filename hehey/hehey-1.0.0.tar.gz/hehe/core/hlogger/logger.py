# -*- coding: utf-8 -*-

from .utils import CommonUtil
import logging
import logging.config

"""
 * 日志管理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  基本示例
 *  使用默认日志器写日志信息
 *  he.app.log.info("太帮忙了订单")
 *  使用自定义日志器hehe 写日志信息
 *  he.app.log.hehe.info("太帮忙了订单")
 *  
 *  日志配置:
 *   请参考python logging 模块
 * 
 *</pre>
 *<B>日志：</B>
 *<pre>
 *  略
 *</pre>
 *<B>注意事项：</B>
 *<pre>
 *  略
 *</pre>
"""
class LogManager():

    '''
    :type hehe: logging.Logger

    '''

    def __init__(self,**attrs):

        # 日志规则配置
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.rules = {
            # 'version': 1,  # 保留字
            # 'disable_existing_loggers': False,  # 禁用已经存在的logger实例
            # # 日志文件的格式
            # 'formatters': {
            #     # 详细的日志格式
            #     'standard': {
            #         'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
            #                   '[%(levelname)s][%(message)s]'
            #     },
            #     # 简单的日志格式
            #     'simple': {
            #         'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
            #     },
            #     # 定义一个特殊的日志格式
            #     'collect': {
            #         'format': '%(message)s'
            #     }
            # },
            # # 过滤器
            # 'filters': {
            #     'require_debug_true': {
            #         '()': 'django.utils.log.RequireDebugTrue',
            #     },
            # },
            # # 处理器
            # 'handlers': {
            #     # 在终端打印
            #     'console': {
            #         'level': 'DEBUG',
            #         'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            #         'class': 'logging.StreamHandler',  #
            #         'formatter': 'simple'
            #     },
            #     # 默认的
            #     'default': {
            #         'level': 'INFO',
            #         'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            #         'filename': os.path.join(BASE_LOG_DIR, "xxx_info.log"),  # 日志文件
            #         'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            #         'backupCount': 3,  # 最多备份几个
            #         'formatter': 'standard',
            #         'encoding': 'utf-8',
            #     },
            #     # 专门用来记错误日志
            #     'error': {
            #         'level': 'ERROR',
            #         'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            #         'filename': os.path.join(BASE_LOG_DIR, "xxx_err.log"),  # 日志文件
            #         'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            #         'backupCount': 5,
            #         'formatter': 'standard',
            #         'encoding': 'utf-8',
            #     },
            #     # 专门定义一个收集特定信息的日志
            #     'collect': {
            #         'level': 'INFO',
            #         'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            #         'filename': os.path.join(BASE_LOG_DIR, "xxx_collect.log"),
            #         'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            #         'backupCount': 5,
            #         'formatter': 'collect',
            #         'encoding': "utf-8"
            #     }
            # },
            # 'loggers': {
            #     # 默认的logger应用如下配置
            #     '': {
            #         'handlers': ['default', 'console', 'error'],  # 上线之后可以把'console'移除
            #         'level': 'DEBUG',
            #         'propagate': True,  # 向不向更高级别的logger传递
            #     },
            #     # 名为 'collect'的logger还单独处理
            #     'collect': {
            #         'handlers': ['console', 'collect'],
            #         'level': 'INFO',
            #     }
            # },
        }

        # 默认日志
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.defaultLogger = '';

        if attrs:
            CommonUtil.setAttrs(self,attrs)

        self._init();


    def getLogger(self,name = ''):
        """
        :rtype:logging.Logger
        :return:
        """
        if not name:
            name = self.defaultLogger

        return logging.getLogger(name);

    def getDefaultLogger(self):
        """
        :rtype:logging.Logger
        :return:
        """
        if hasattr(self,'_logger'):
            return getattr(self,'_logger')

        logger = logging.getLogger(self.defaultLogger);
        setattr(self,'_logger',logger)

        return logger

    def _init(self):

        # 加载配置
        rules = self.rules.copy();
        logging.config.dictConfig(rules)

        return ;


    def log(self,level,msg,loggerName = '', *args, **kwargs):

        return self.getLogger(loggerName).log(level,msg, *args, **kwargs)

    def debug(self,msg,loggerName = '', *args, **kwargs):

        return self.getLogger(loggerName).debug(msg, *args, **kwargs)

    def info(self,msg,loggerName = '', *args, **kwargs):

        return self.getLogger(loggerName).info(msg, *args, **kwargs)

    def warning(self,msg,loggerName = '', *args, **kwargs):

        return self.getLogger(loggerName).warning(msg, *args, **kwargs)

    def error(self,msg,loggerName = '', *args, **kwargs):

        return self.getLogger(loggerName).error(msg, *args, **kwargs)

    def critical(self,msg,loggerName = '', *args, **kwargs):

        return self.getLogger(loggerName).critical(msg, *args, **kwargs)

    def exception(self,msg,loggerName = '', *args, exc_info=True, **kwargs):

        return self.getLogger(loggerName).exception(msg, *args, exc_info, **kwargs)


    def __getattr__(self, name):
        """
        :rtype:logging.Logger
        :return:
        """
        return self.getLogger(name)




