import cv2
import numpy as np


def sobel(img):
    """
    Quick approximation of the 1st order derivative (Sobel method).

    :param img: cv2/np.ndarray
    """
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
    grad = cv2.addWeighted(np.absolute(gx), 0.5, np.absolute(gy), 0.5, 0)
    return grad
