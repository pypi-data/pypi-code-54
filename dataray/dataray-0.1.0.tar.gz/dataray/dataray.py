from dataray.helper import structure_summary


class DataRay:
    def ray(self):
        def wrapper(request_func, *args, **kwargs):
            response = request_func(*args, **kwargs)
            structure_summary(response)
            return request_func
        return wrapper




