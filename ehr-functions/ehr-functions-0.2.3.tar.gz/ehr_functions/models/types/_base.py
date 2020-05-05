class Model:
    def __init__(self, multiple_output=False):
        self.multiple_output = multiple_output

    def train(self, x, y):
        raise NotImplementedError

    def predict(self, x):
        raise NotImplementedError
