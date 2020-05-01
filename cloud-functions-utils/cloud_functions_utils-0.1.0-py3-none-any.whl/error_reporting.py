from google.cloud.error_reporting import Client


class error_reporting:
    def __init__(self, func):
        self._func = func
        self._client = Client()

    def __call__(self, *args, **kwargs):
        try:
            self._func(*args, **kwargs)
        except Exception as error:
            self._client.report_exception()
            raise error
