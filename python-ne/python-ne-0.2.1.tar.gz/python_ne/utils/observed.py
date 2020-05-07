class Observed:

    def __init__(self):
        self.observers = []

    def notify_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.notify(*args, **kwargs)

    def add_observer(self, observer):
        self.observers.append(observer)
