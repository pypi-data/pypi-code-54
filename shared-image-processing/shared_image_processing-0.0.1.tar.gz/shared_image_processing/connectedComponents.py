"""Contains functions related to connected components algorithms."""
import numpy as np
from scipy.ndimage.measurements import label

def getBiggestComp(image):
    """ Uses connected components to get the breast """
    structure = np.ones([3,3], dtype=np.int) # Relational matrix (8-connected)
    # Run connected components to label the various connected components
    labeled_image, _ = label(image, structure=structure) 

    counts = np.bincount(labeled_image.flatten())
    ind = np.argmax(counts[1:]) + 1
    biggestComp = (labeled_image == ind).astype(np.uint8)

    return biggestComp

def get_seed_region(image, seed_coords):
    """ Gets the seed region  """
    structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.int) # Relational matrix (4-connected)

    # Run connected components to label the various connected components
    labeled_image, _ = label(image, structure=structure) 

    seed_label = labeled_image[seed_coords[1], seed_coords[0]]

    seed_component = (labeled_image == seed_label).astype(np.uint8)

    return seed_component
