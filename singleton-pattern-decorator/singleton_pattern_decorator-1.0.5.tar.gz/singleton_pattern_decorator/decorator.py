"""
"""


class Singleton:
    """
    """

    def __init__(self, cls):
        self._cls_wrapper = cls
        self.__instance = None

    """
    """

    @property
    def instance(self):
        return self.__instance

    """
    """

    @property
    def wrapper(self):
        return self._cls_wrapper

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = self._cls_wrapper(*args, **kwargs)

        return self.__instance


"""
"""


def singleton(cls):
    return Singleton(cls)
