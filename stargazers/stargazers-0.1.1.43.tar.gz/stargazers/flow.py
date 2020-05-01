import cv2
import numpy as np


def get_flow(img_1, img_2, *, 
        pyr_scale=0.5, # own old 0.9
        levels=3,      # own old 20
        winsize=25,    # own old 40
        iters=3,       # own old 8
        poly_n=7,      # own old 5
        poly_s=0.7,    # own old 1.1
        flags=0        # usually 0
    ):
    """
    Calculates the optical flow from img_1 to img_2.
    
    :param img_1: cv2/np.ndarray
    :param img_2: cv2/np.ndarray
    ---- Keyword only ----
    The parameters of cv2.calcOpticalFLowFarneback:
        `pyr_scale`, `levels`, `winsize`, `iters`, `poly_n`, `poly_s` and
        `flags`
    """
    if len(img_1.shape) == 3:
        gray_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    else:
        gray_1 = img_1
    if len(img_2.shape) == 3:
        gray_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
    else:
        gray_2 = img_2
    flow = cv2.calcOpticalFlowFarneback(
        gray_1,   # first image
        gray_2,   # second image
        None,     # flow (previous)
        pyr_scale,
        levels,
        winsize,
        iters,
        poly_n,
        poly_s,
        flags
    )
    return flow


def warp(img, flow):
    """
    Warps img according to flow.

    :param img: cv2/np.ndarray image
    :param flow: cv2 optical flow
    """
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv2.remap(img, flow, None, cv2.INTER_LANCZOS4)
    return res

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr


def tween(img1, img2, flow, alpha):
    """
    In-betweens img1 and img2 according to flow and alpha.

    :param img1: first image of the sequence
    :param img2: final image of the sequence
    :param flow: cv2 optical flow
    :param alpha: degree (0..1) of the in-between (0 is fully img1, 1 is fully
        img2)
    """
    im1 = warp(img1, flow * alpha)
    im2 = warp(img2, -flow * (1 - alpha))
    ret = im1.astype(np.float32) * (1 - alpha) + im2.astype(np.float32) * alpha
    return ret.astype(np.uint8)
