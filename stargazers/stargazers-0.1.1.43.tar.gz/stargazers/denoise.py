import cv2
import numpy as np
from scipy import signal


STREL_CIRCLE_5 = np.array([
    [  0,  1,  1,  1,  0],
    [  1,  1,  1,  1,  1],
    [  1,  1,  1,  1,  1],
    [  1,  1,  1,  1,  1],
    [  0,  1,  1,  1,  0],
])

STREL_DIAMOND_5 = np.array([
    [  0,  0,  1,  0,  0],
    [  0,  1,  1,  1,  0],
    [  1,  1,  1,  1,  1],
    [  0,  1,  1,  1,  0],
    [  0,  0,  1,  0,  0],
])

STREL_SQUARE_5 = np.ones((5, 5))


#@profile
def despeckle(img, strel, t=3, func=np.nanmedian):
    """
    Despeckles an image using a structuring element an averaging function and
    a threshold.
    :param img: cv2/np.ndarray image
    :param strel: structuring element (np.ndarray), assumed square shape
    :param t: threshold to determine when is it appropriate to despeckle
    :param func: averaging function (defaults to np.nanmedian)
    """
    out = img.copy()
    img = img.astype(np.float32)
    strel_ones = int(strel.sum())
    avg = np.zeros((img.shape[0], img.shape[1], strel_ones), dtype=np.float32)
    margin = strel.shape[0] // 2  # we assume a square structuring element
    height, width = img.shape[:2]
    for y in range(margin, height - margin):
        for x in range(margin, width - margin):
            box = img[y - margin: y + margin + 1, x - margin: x + margin + 1].copy()
            box[margin, margin] = np.NaN
            # values = box[strel == 1]
            # avg[y, x] = values
            avg[y, x] = box[strel == 1]
    avg = func(avg, axis=2)
    th = avg * t
    out[img > th] = avg[img > th]
    return out


#@profile
def despeckle_conv(img, strel, t=3, debug=False):
    """
    Despeckles an image using a structuring element and a threshold.

    It uses a mean averaging function, applied directly by working applying a
    convolution to the image and then checking against that. This allows for
    a speedup, but the doesn't give results as good as the median.
    """
    out = img.copy()
    img = img.astype(np.float32)
    margin = strel.shape[0] // 2  # we assume a square structuring element
    strel_ones = int(strel.sum())
    strel[margin, margin] = 0
    avg = signal.convolve2d(img, strel, boundary='symm', mode='same')
    avg /= strel_ones
    th = avg * t
    out[img > th] = avg[img > th]
    if debug:
        return out, avg
    return out

# profile run of despeckle
# this points that we should get an even lazier version
r"""
C:\Users\bruco\Documents\GitHub\stargazers>kernprof -lv perf.py
Wrote profile results to perf.py.lprof
Timer unit: 1e-07 s

Total time: 338.454 s
File: C:\Users\bruco\Documents\GitHub\stargazers\stargazers\denoise.py
Function: despeckle at line 24

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    24                                           @profile
    25                                           def despeckle(img, strel, t=3, func=np.nanmedian):
    26                                               '''
    27                                               Despeckles an image using a structuring element an averaging function and
    28                                               a threshold.
    29                                               :param img: cv2/np.ndarray image
    30                                               :param strel: structuring element (np.ndarray), assumed square shape
    31                                               :param t: threshold to determine when is it appropriate to despeckle
    32                                               :param func: averaging function (defaults to np.nanmedian)
    33                                               '''
    34        10     208870.0  20887.0      0.0      out = img.copy()
    35        10     879853.0  87985.3      0.0      img = img.astype(np.float32)
    36        10       4875.0    487.5      0.0      strel_ones = int(strel.sum())
    37        10     100780.0  10078.0      0.0      avg = np.zeros((img.shape[0], img.shape[1], strel_ones), dtype=np.float32)
    38        10        321.0     32.1      0.0      margin = strel.shape[0] // 2  # we assume a square structuring element
    39        10        218.0     21.8      0.0      height, width = img.shape[:2]
    40     18570     107856.0      5.8      0.0      for y in range(margin, height - margin):
    41  37064320  227045665.0      6.1      6.7          for x in range(margin, width - margin):
    42  37045760  783025224.0     21.1     23.1              box = img[y - margin: y + margin + 1, x - margin: x + margin + 1].copy()
    43  37045760  346476847.0      9.4     10.2              box[margin, margin] = np.NaN
    44  37045760 1010781140.0     27.3     29.9              values = box[strel == 1]
    45  37045760  516406365.0     13.9     15.3              avg[y, x] = values
    46        10  497802206.0 49780220.6     14.7      avg = func(avg, axis=2)
    47        10     703979.0  70397.9      0.0      th = avg * t
    48        10     997043.0  99704.3      0.0      out[img > th] = avg[img > th]
    49        10        430.0     43.0      0.0      return out
"""
