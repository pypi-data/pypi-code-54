__all__ = ['NotRegistered', 'AlreadyRegistered', 'ImproperlyConfigured']


class NotRegistered(Exception):
    pass


class AlreadyRegistered(Exception):
    pass


class ImproperlyConfigured(Exception):
    pass
