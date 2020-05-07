class ModelAdapter:

    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        raise NotImplementedError()

    def add_dense_layer(self, **kwargs):
        raise NotImplementedError()

    def get_weights(self):
        raise NotImplementedError()

    def set_weights(self, weights):
        raise NotImplementedError()

    def predict(self, obs):
        raise NotImplementedError()

    def initialize(self):
        raise NotImplementedError()

    def get_layers(self):
        raise NotImplementedError()

    def save(self, file_path):
        raise NotImplementedError()

    @staticmethod
    def new_instance():
        raise NotImplementedError()

    @staticmethod
    def load(file_path):
        raise NotImplementedError()
