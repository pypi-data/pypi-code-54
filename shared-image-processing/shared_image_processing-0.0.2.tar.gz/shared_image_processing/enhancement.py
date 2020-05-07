"""Contains image enhancement functions."""
import logging
import numpy as np

def contrast_stretch(image, min_I, max_I):
    """Apply the contrast stretch transformation to the image.

    All values < min_I will be 0 and all values > max_I will be 1.
    
    Parameters
    ----------
    image : ndarray
        Image data
    min_I : int
        Intensity floor
    max_I : int
        Intensity ceiling
    
    Returns
    -------
    ndarray
        Contrast-stretch image
    """
    # copy image
    image_copy = image.copy()

    try: 
        # Apply transform
        A = np.array([[min_I, 1], [max_I, 1]])
        B = [0, 1]

        [slope, intercept] = np.linalg.solve(A, B)

        image_copy[np.where((image_copy >= min_I) & (image_copy <= max_I))] = \
            slope * image_copy[np.where((image_copy >= min_I) & (image_copy <= max_I))] + intercept

        image_copy[np.where(image < min_I)] = 0
        image_copy[np.where(image > max_I)] = 1
    except np.linalg.LinAlgError as err:
        # Ignore singular matrix issues and raise other issues
        if 'Singular matrix' in str(err):
            logging.warning('SINGULAR MATRIX: NOT DOING CONTRAST STRETCH')
        else:
            raise

    return image_copy