import json

from python_ne.core.neural_network.dense_layer import DenseLayer

LAYER_LEY = 'layers'


def save_as_json(nn, file_path):
    file = open(file_path, 'w+')
    layers = []
    for layer in nn.layers:
        layer_weights = layer.get_weights()
        layers.append({
            'units': layer.units,
            'input_shape': layer.input_shape,
            'activation': layer.activation.__name__,
            'weights': layer_weights[0].tolist(),
            'bias': layer_weights[1].tolist()
        })
    file.write(json.dumps({LAYER_LEY: layers}))
    file.close()


def load_from_json(file_path):
    file = open(file_path)
    layers = json.loads(file.read())['layers']
    file.close()
    return layers
