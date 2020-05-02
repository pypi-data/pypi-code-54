

def only_once(user_function):
    cache = {}

    def decorate(*args, **kwargs):
        object_id = id(args[0])
        cache_key = str(object_id) + user_function.__name__
        if cache_key not in cache:
            cache[cache_key] = user_function(*args, **kwargs)
        return cache[cache_key]
    return decorate
