import os
import logging
from logging.handlers import TimedRotatingFileHandler
import codecs
from logging import FileHandler
import gzip
import time
import multiprocessing


class SafeTimeFileHandler(FileHandler):
    def __init__(self, filename, mode, encoding=None, delay=0):
        """
        Use the specified filename for streamed logging
        """
        if codecs is None:
            encoding = None
        FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y-%m-%d"
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.

        Always check time
        """
        try:
            if self.check_baseFilename(record):
                self.build_baseFilename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_baseFilename(self, record):
        """
        Determine if builder should occur.

        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        timeTuple = time.localtime()

        # 当前时间与预设时间不一致(过了一天)或者检测到还没有rotation
        if self.suffix_time != time.strftime(self.suffix, timeTuple) or not os.path.exists(
                self.baseFilename + '.' + self.suffix_time):
            return 1
        else:
            return 0

    def build_baseFilename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = 'a'
        if not self.delay:
            self.stream = self._open()


class LoggerAdapter():
    def __init__(self, logger, extra):
        self.logger = logger
        self.extra = extra

    def process(self, msg, kwargs):
        """
        Process the logging message and keyword arguments passed in to
        a logging call to insert contextual information. You can either
        manipulate the message itself, the keyword args or both. Return
        the message and kwargs modified (or not) to suit your needs.
        Normally, you'll only need to override this one method in a
        LoggerAdapter subclass for your specific needs.14"""
        kwargs["extra"] = self.extra
        return msg, kwargs

    def debug(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.info(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.info(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.info(msg, *args, **kwargs)


class GZipRotator():
    """
    Roatator callable as suggested by
    https://docs.python.org/3.3/library/logging.handlers.html?highlight=logging.handler#logging.handlers.BaseRotatingHandler
    """
    def __call__(self, source, dest):
        os.rename(source, dest)
        f_in = open(dest, 'rb')
        f_out = gzip.open("%s.gz" % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)


def get_logger(name, level='info', log_dir=None, daily_handler=False, keep=1095, log_fmt=None,
               compress=False):
    """
    日志记录封装，线程安全
    :param name: 日志文件名
    :param level: 日志等级
    :param log_dir: 日志路径，默认为../log/
    :param daily_handler: 是否每天滚动日志
    :param keep: 日志文件保存时间，默认60天
    :param log_fmt: 日志的format
    :return: logger
    """
    LOG_PATH = os.path.join(os.path.dirname(os.getcwd()), 'log')
    level_lookuper = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARNING,
                      'error': logging.ERROR}
    if log_fmt is None:
        log_fmt = '%(asctime)s\tFile \"%(filename)s\"\t%(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    if log_dir is None:
        log_dir = os.path.join(LOG_PATH, name + '_log')
    if not os.path.exists(os.path.dirname(log_dir)):
        os.makedirs(os.path.dirname(log_dir))
    logger = logging.getLogger(name)
    logger.setLevel(level=level_lookuper[level])
    if not logger.handlers:
        if daily_handler:
            handler = TimedRotatingFileHandler(filename=log_dir, when="midnight", interval=1,
                                               backupCount=keep, encoding='utf-8')
            if compress:
                handler.rotator = GZipRotator()
            handler.setFormatter(formatter)
            handler.setLevel(level=level_lookuper[level])
        else:
            handler = logging.FileHandler(log_dir, encoding='utf-8')
            handler.setFormatter(formatter)
            handler.setLevel(level=level_lookuper[level])
        logger.addHandler(handler)
    return logger


def get_save_daily_logger(name, level='info', log_dir=None, log_fmt=None):
    """
    非常简单的方式获取多进程状态下的每日rotation的日志记录器。
    日志会被记录到log_dir/name_log.current_date文件下
    但由于用的是直接寻找当前输出文件目录的办法，
    无法进行原来logging模块意义上的rotation和压缩，
    因为每个进程不会去判断是否应该rotation,
    而是直接去正确的文件打印日志（不关心其他进程在干嘛）
    目前想到的优化是，单独做一个定时日志压缩的服务来解决这个问题。
    :param name:
    :param level:
    :param log_dir:
    :param log_fmt:
    :return:
    """
    LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'log')
    level_lookuper = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARNING,
                      'error': logging.ERROR}
    if log_fmt is None:
        log_fmt = '%(asctime)s\tFile \"%(filename)s\"\t%(levelname)s pid【%(process)s】: %(message)s'
    formatter = logging.Formatter(log_fmt)
    if log_dir is None:
        log_dir = os.path.join(LOG_PATH, name, name + '_log')
    if not os.path.exists(os.path.dirname(log_dir)):
        os.makedirs(os.path.dirname(log_dir))
    logger = logging.getLogger(name)
    logger.setLevel(level=level_lookuper[level])
    if not logger.handlers:
        handler = SafeTimeFileHandler(filename=log_dir, encoding='utf-8', mode='a')
        handler.setFormatter(formatter)
        handler.setLevel(level=level_lookuper[level])
        logger.addHandler(handler)
    return logger


def get_logger_prod(name, level='info', log_dir=None, daily_handler=False, keep=1095, log_fmt=None, compress=False):
    """
    日志记录
    :param name: 日志文件名
    :param level: 日志等级
    :param log_dir: 日志路径，默认为../log/
    :param daily_handler: 是否每天滚动日志
    :param keep: 日志文件保存时间，默认60天
    :param log_fmt: 日志的format
    :return: logger
    """
    LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'log')
    level_lookuper = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARNING,
                      'error': logging.ERROR}
    if log_fmt is None:
        log_fmt = '%(asctime)s\tFile \"%(filename)s\"\t%(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    if log_dir is None:
        log_dir = os.path.join(LOG_PATH, name, name + '_log')
    if not os.path.exists(os.path.dirname(log_dir)):
        os.makedirs(os.path.dirname(log_dir))
    logger = logging.getLogger(name)
    logger.setLevel(level=level_lookuper[level])
    if not logger.handlers:
        if daily_handler:
            handler = TimedRotatingFileHandler(filename=log_dir, when="midnight", interval=1,
                                               backupCount=keep, encoding='utf-8')
            if compress:
                handler.rotator = GZipRotator()
            handler.setFormatter(formatter)
            handler.setLevel(level=level_lookuper[level])
        else:
            handler = logging.FileHandler(log_dir, encoding='utf-8')
            handler.setFormatter(formatter)
            handler.setLevel(level=level_lookuper[level])
        logger.addHandler(handler)
    return logger


def log_listener(queue, name,
                 level='info', log_dir=None, daily_handler=False, keep=1095,
                 log_fmt='%(asctime)s\tFile \"%(filename)s\"\t%(levelname)s pid【%(process)s】: %(message)s',
                 compress=False):
    """
    多进程日志消费端
    :param queue: 队列实例
    :param name: 日志实例名称
    :param level: 日志级别
    :param log_dir: 日志目录
    :param daily_handler: 是否每日进行rotation
    :param keep: 日志生命周期，但目前似乎有BUG，如果服务重启会重写计算时间
    :param log_fmt: 日志格式，可自定义
    :param compress: 是否压缩
    :return:
    """
    if not isinstance(queue, multiprocessing.queues.Queue):
        raise AssertionError("arg queue must be class of `multiprocessing.queues.Queue`")
    # 在 listener 里生成logger实例
    logger = get_logger_prod(name, level=level, log_dir=log_dir,
                             daily_handler=daily_handler, keep=keep,
                             log_fmt=log_fmt, compress=compress)
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


def get_sender_logger(queue, log_name):
    """
    消息生产端
    :param queue: queque
    :param log_name: logger实例名称
    :return:
    """
    handler = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger(log_name)
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)
    return root


def logger_time_it(func):
    """
    抽取函数专用计时器装饰器，不能用于他处, 自动记录函数运行时间
    :param func:
    :return:
    """
    def make_decorater(*args, **kwargs):
        # 获取传入类的属性(日志记录器)
        logger = args[0].logger
        t0 = time.time()
        result = func(*args, **kwargs)
        logger.info("函数【%s】, 运行耗时%.3f秒"
                    % (func.__name__,
                       time.time() - t0))
        return result
    return make_decorater

if __name__ == '__main__':
    pass
    # queue = multiprocessing.Queue()
    # listener = multiprocessing.Process(target=log_listener, args=(queue,))
    # listener.start()
    # workers = []
    # for i in range(3):
    #     worker = multiprocessing.Process(target=worker_process, args=(queue, worker_configurer, i))
    #     workers.append(worker)
    #     worker.start()

