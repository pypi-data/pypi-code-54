class ValidationException(BaseException):
    def __init__(self, *args):
        self.errors = {args[0]: args[1]}

    def __str__(self):
        return f'{self.errors}'
