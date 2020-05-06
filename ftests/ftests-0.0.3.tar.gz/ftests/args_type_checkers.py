def assert_isinstance(obj, cls, message=None):
    if not isinstance(obj, cls):
        raise TypeError(message) if message else TypeError
