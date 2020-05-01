import cv2
import numpy as np


def levels(img, black=0, white=255):
    """
    Modifies the levels of an image. Assumes a 0-255 uint8 image. Casts to
    float32 inbetween. If the image is in a 0..1 range, direct manipulation
    is prefered.

    :param img: BGR cv2 image/nump.ndarray
    :param black: black point for the image
    :param white: white point for the image
    return: BGR cv2 image/numpy.ndarray
    """
    temp = img.astype(np.float32)
    temp -= black
    white = white - black
    temp /= white
    temp = np.maximum(0, np.minimum(1, temp))
    temp *= 255
    return temp.astype(np.uint8)


def saturate(img, sat):
    """
    Modifies the saturation of an image.

    :param img: BGR cv2 image/numpy.ndarray
    :param sat: real valued scalar, to multiply the saturation channel
    :return: BGR cv2 image/numpy.ndarray
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv2 = hsv.astype(np.float32)
    mult = np.ones(hsv.shape)
    mult[:,:,1] *= sat
    hsv2 = cv2.multiply(hsv.astype(np.float64), mult)
    hsv2 = np.minimum(255, hsv2)
    hsv2 = hsv2.astype(np.uint8)
    hsv2 = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)
    return hsv2


def temperature(img, temp):
    """
    http://www.askaswiss.com/2016/02/how-to-manipulate-color-temperature-opencv-python.html
    """
    return None


def threshold(img, thresh):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret = np.zeros(img.shape, dtype=img.dtype)
    ret[img > thresh] = 255
    return ret
