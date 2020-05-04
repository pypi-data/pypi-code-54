import threading
from abc import ABC, abstractmethod


class Observer(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def callback(self, caller, args):
        pass


class Observable(ABC):
    def __init__(self):
        super().__init__()
        self.__listeners = []
        self.__lock = threading.RLock()

    def notify_listeners(self, args=None):
        self.__lock.acquire()
        try:
            for listener in self.__listeners:
                listener.callback(self, args)
        finally:
            self.__lock.release()

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def remove_listener(self, listener):
        self.__listeners.remove(listener)
