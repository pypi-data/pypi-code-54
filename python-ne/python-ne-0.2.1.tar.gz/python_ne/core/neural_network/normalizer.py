import numpy as np


def normalize(x):
    """keras.utils.normalize but directly here to avoid importing"""

    axis = -1
    order = 2
    l2 = np.atleast_1d(np.linalg.norm(x, order, axis))
    l2[l2 == 0] = 1
    return ( x / np.expand_dims(l2, axis) )[0]
