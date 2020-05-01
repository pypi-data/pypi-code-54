import cv2
import numpy as np


def translate(img, trans):
    """
    Translates an image using an affine transform.

    :param img: cv2/np.ndarray
    :param trans: (tx, ty) translation tuple
    :return: cv2/np.ndarray
    """
    tx, ty = trans
    h, w = img.shape[:2]
    aff_mat = np.float32([
        [1, 0, tx],
        [0, 1, ty],
    ])
    out = cv2.warpAffine(img, aff_mat, (w, h))
    return out

