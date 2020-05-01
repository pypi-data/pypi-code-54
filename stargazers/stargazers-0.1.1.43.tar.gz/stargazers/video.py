import cv2
import numpy as np


class IterableVideo:
    def __init__(self, path):
        self.path = path
    
    def __iterator(self):
        cap = cv2.VideoCapture(self.path)
        status, frame = cap.read()
        while status:
            yield frame
            status, frame = cap.read()
        cap.release()
    
    def __iter__(self):
        return self.__iterator()


def stabilize(video, writer):
    """
    Stabilizes a video and outputs to a writer.

    :param video: an iterable of cv2 images/np.ndarrays.
    :param writer: cv2.VideoWriter object.
    """
    pass
