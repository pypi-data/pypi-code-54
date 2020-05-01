# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image


def from_pil(pimg):
    pimg = pimg.convert(mode='RGB')
    nimg = np.array(pimg)
    return nimg


def to_pil(nimg):
    return Image.fromarray(np.uint8(nimg))
