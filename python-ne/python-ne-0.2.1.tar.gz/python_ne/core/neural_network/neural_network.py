import numpy as np

import python_ne.core.neural_network.saving as saving
from python_ne.core.neural_network import activations
from python_ne.core.neural_network.dense_layer import DenseLayer


class NeuralNetwork:

    def __init__(self):
        self.layers = []

    def initialize(self):
        """
        Initialize all nn layers.

        This method is not required to be called. Layer initialization will be performed when predict is callled.
        Can be used to initialize the layers without calling predict.
        """

        input_shape = None
        for index, layer in enumerate(self.layers):
            if index == 0:
                # dont need to set input shape here, first layer will always have an input shape
                layer.initialize()
            else:
                # current layer input shape = prev layer neuron count
                layer.input_shape = input_shape
                layer.initialize()

            #  next layer input shape
            input_shape = (layer.units,)

    def predict(self, xs):
        input_shape = None
        output = None
        for index, layer in enumerate(self.layers):
            layer.input_shape = layer.input_shape if index == 0 else input_shape
            layer.initialize()
            input_shape = (layer.units,)
            output = layer.feedforward(xs if index == 0 else output)

        return output

    def add(self, layer):
        self.layers.append(layer)

    def save(self, file_path):
        saving.save_as_json(self, file_path)

    @staticmethod
    def load(file_path):
        layers = saving.load_from_json(file_path)

        nn = NeuralNetwork()

        for layer in layers:
            nn.add(
                DenseLayer(
                    units=layer['units'],
                    input_shape=tuple(layer['input_shape']),
                    activation=layer['activation'],
                    weights=(np.array(layer['weights']), np.array(layer['bias']))
                )
            )

        return nn
