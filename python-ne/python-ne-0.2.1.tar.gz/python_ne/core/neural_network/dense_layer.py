import numpy as np

from python_ne.core.neural_network import activations


class DenseLayer:

    def __init__(self, units, activation, input_shape=None, weights=(None, None,)):
        self.units = units
        self.activation = activations.get_activation_from_str(activation)
        self.input_shape = input_shape
        self.weights, self.bias = weights

    def initialize(self):
        if self.weights is not None and self.bias is not None:
            return

        self.bias = np.random.uniform(low=-1, high=1, size=(self.units,))
        # number os neurons of the prev layer and number of neurons of this layer, shape = (input_shape[0], units)
        self.weights = np.random.uniform(low=-1, high=1, size=(self.input_shape[0], self.units))

    def feedforward(self, xs):
        if xs.shape != self.input_shape:
            raise Exception('Dense layer got an invalid input shape.' +
                            f' Was expecting {self.input_shape} but got {xs.shape} instead')

        output = xs.dot(self.weights)
        return self.activation(output + self.bias)

    def get_weights(self):
        return np.copy(self.weights), np.copy(self.bias)

    def set_weights(self, weights):
        self.weights, self.bias = weights
