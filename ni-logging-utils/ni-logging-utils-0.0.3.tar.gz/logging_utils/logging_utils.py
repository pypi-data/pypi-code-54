import functools
import logging
import time


class Chronometer:

    def __init__(self, function_name=None):
        self.__func_name = function_name
        self.__logger = logging.getLogger(function_name)

    def __call__(self, func, *args, **kwargs):

        def decorated(*args, **kwargs):
            self.__logger.info(f'Lancement de {self.__func_name}')
            start = time.time()
            value = func(*args, **kwargs)
            end = time.time()
            self.__logger.debug(f'Fin de {self.__func_name} en {end - start} secondes')
            return value

        return decorated


class LogDecorator:

    def __init__(self, decorator_log='decorator-log', resume=False):
        self.__logger = logging.getLogger(decorator_log)
        self.__resume = resume

    def __call__(self, func):

        @functools.wraps(func)
        def decorated(*args, **kwargs):

            def to_message(value):
                if self.__resume and isinstance(value, list):
                    return f"Function return {len(value)} values"
                return f"Function return {value}"

            try:
                self.__logger.debug(f"{func.__name__} - {args} - {kwargs}")
                result = func(*args, **kwargs)
                self.__logger.debug(to_message(result))
                return result
            except Exception as exception:
                self.__logger.debug(f"Exception: {exception}")
                raise exception

        return decorated
