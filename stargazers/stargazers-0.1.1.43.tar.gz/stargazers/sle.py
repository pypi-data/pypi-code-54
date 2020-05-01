"""
Simple Linear Editor
(to finally make aurora videos in one encoding)
"""
import cv2
import numpy as np


from .video import IterableVideo


# check https://superuser.com/questions/277642/how-to-merge-audio-and-video-file-in-ffmpeg
class Scene:
    """
    One scene that can have opening, closing and/or compose two (or more) other
    Scenes.
    """
    def __init__(self, source):
        self.source = source
        self.frame_counter = 0
    
    def render(self):
        """
        Returns one frame of the scene.
        """
        self.frame_counter += 1
        return None


class LinearEditor:
    pass
