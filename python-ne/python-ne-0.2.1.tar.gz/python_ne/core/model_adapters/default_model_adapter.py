from python_ne.core.model_adapters.model_adapter import ModelAdapter
from python_ne.core.model_adapters.default_dense_layer_adapter import DefaultDenseLayerAdapter
from python_ne.core.neural_network import activations
from python_ne.core.neural_network.dense_layer import DenseLayer
from python_ne.core.neural_network.neural_network import NeuralNetwork


class DefaultModelAdapter(ModelAdapter):

    @staticmethod
    def new_instance():
        return DefaultModelAdapter()

    def initialize(self):
        self.model.initialize()

    def add_dense_layer(self, **kwargs):
        self.model.add(DenseLayer(**kwargs))

    def build_model(self):
        return NeuralNetwork()

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights()

    def predict(self, obs):
        return self.model.predict(obs)

    def get_layers(self):
        return [DefaultDenseLayerAdapter(layer) for layer in self.model.layers]

    def save(self, file_path):
        self.model.save(file_path)

    @staticmethod
    def load(file_path):
        nn = NeuralNetwork.load(file_path)
        new_adapter = DefaultModelAdapter()
        new_adapter.model = nn
        return new_adapter
