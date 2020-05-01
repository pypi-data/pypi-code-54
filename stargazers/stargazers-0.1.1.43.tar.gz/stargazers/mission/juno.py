import cv2
import numpy as np


def strip_to_sequence(img, strip_height=128):
    """
    Receives a grayscale image from Juno and converts it into a sequence
    of BGR-images. Yields one of these images at a time until ending.

    :param img: cv2/np.ndarray image from JunoCam.
    :yields: BGR-images
    """
    allstrips = strip_height * 3
    shape = img.shape[:2]
    ypos = 0
    counts = shape[0] // allstrips
    for _ in range(counts):
        allone = img[ypos:ypos + allstrips, :]
        ret = np.zeros((strip_height, shape[1], 3), dtype=np.uint8)
        ret[:,:,0] = allone[strip_height * 2: strip_height * 3, :]
        ret[:,:,1] = allone[strip_height    : strip_height * 2, :]
        ret[:,:,2] = allone[0               : strip_height,     :]
        ypos += allstrips
        yield ret