# -*- coding=utf-8 -*-
"""YOLO2 preprocess."""
import numpy as np
from PIL import Image


def image_to_tensor(image: Image) -> np.ndarray:
    """
    Realise preprocess for an input pillow image and convert it to numpy array.

    Parameters
    ----------
    image
        An input image to be processed.

    Returns
    -------
    tensor
        Preprocessed numpy array.
    """
    image = image.resize((608, 608), Image.BICUBIC)
    image = image.convert('RGB')
    tensor = np.asarray(image)
    tensor = tensor / 255.0
    assert tensor.shape == (608, 608, 3)
    return tensor
