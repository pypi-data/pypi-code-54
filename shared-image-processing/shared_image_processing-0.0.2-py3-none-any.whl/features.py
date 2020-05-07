"""Contains functions used to derive features from images."""
import logging
import numpy as np
import cv2

def calc_image_prof(image, size=(200, 200)):
    """Calculate the mean horizontal and vertical profiles.
    
    Parameters
    ----------
    image : ndarray
        Image data
    size : tuple
        Specific size of the intermediate square image that the profiles are calculated from
    
    Returns
    -------
    (float[], float[])
        The mean horizontal and vertical profiles
    """
    logging.debug('Calculating the profiles of the image')
    image_square = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    
    hor_profile = np.mean(image_square, axis=0)
    vert_profile = np.mean(image_square, axis=1)

    # plt.subplot(1, 2, 1)
    # plt.imshow(image_square, cmap='bone')
    # plt.subplot(1, 2, 2)
    # plt.plot(np.arange(0, 200), hor_profile, label='Horizontal')
    # plt.plot(np.arange(0, 200), vert_profile, label='Vertical')
    # plt.legend()
    # plt.show()

    logging.debug('Done calculating the profiles of the image')

    return hor_profile, vert_profile