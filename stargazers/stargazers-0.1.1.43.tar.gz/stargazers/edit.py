import cv2
import numpy as np


def alpha_compose(fore, back, mask, debug=False):
    fmask = fore[:,:,3]
    fmask = fmask.astype(np.float32)
    fmask /= 255
    fmask = fmask * mask
    imask = 1 - fmask
    #print(f"fmask: {fmask.shape} imask: {imask.shape} fore: {fore.shape} back: {back.shape}")
    fmask = cv2.cvtColor(fmask, cv2.COLOR_GRAY2BGR)
    imask = cv2.cvtColor(imask, cv2.COLOR_GRAY2BGR)
    if debug:
        return fmask, imask, fore[:,:,:3], back
    out = (fore[:,:,:3] * fmask) + (back * imask)
    return out.astype(np.uint8)

