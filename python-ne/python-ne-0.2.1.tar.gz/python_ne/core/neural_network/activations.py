import numpy as np


def sigmoid(x):
    return 1/(1 + np.exp(-x))


def tanh(x):
    return np.tanh(x)


def get_activation_from_str(string):
    if string == 'sigmoid':
        return sigmoid
    elif string == 'tanh':
        return tanh
    else:
        raise Exception(f' \'{string}\' activation function not found')
