import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap, ListedColormap


def hex_to_rgb(hex):

    hex = hex.replace("#","")
    
    return tuple(int(hex[i:i+2], 16)/255. for i in (0, 2, 4))


class ColorMap(object):

    def __init__(self, *colors, discrete=False, name=None):

        self._colors = colors

        if not discrete:

            self._cmap = LinearSegmentedColormap.from_list(name, self._colors)

        else:

            NotImplementedError()

        if name is not None:
            
            cm.register_cmap(name=name, cmap=self._cmap)

    @property
    def cmap(self):
        return self._cmap
    
    @classmethod
    def from_hex(cls, *hexs, discrete=False, name=None):

        rgb = [hex_to_rgb(hex) for hex in hexs]

        return cls(*rgb, discrete=discrete, name=name)
