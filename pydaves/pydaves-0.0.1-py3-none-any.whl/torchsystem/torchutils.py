import torch.nn as nn


def count_maxpool(block):
    dict_block = dict(block.named_children())
    n_maxpool = 0
    for key in dict_block.keys():
        if 'MaxPool' in dict_block[key]._get_name():
            n_maxpool += 1
    return n_maxpool


def init_params(element):
    if type(element) in [nn.Conv2d]:
        # initializing weights with kaiming normal distribution
        nn.init.kaiming_normal_(element.weight)

        # initializing biases with normal distribution
        nn.init.normal_(element.bias)
