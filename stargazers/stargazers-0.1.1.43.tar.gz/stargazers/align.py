import cv2
import numpy as np


from .flow import get_flow, warp
from .gradients import sobel


# for the moment, I need it here
# gotta think a better place for it

###


def center_align(img_, thresh=128, *, only_matrix=False):
    """
    Estimates the center of gravity of the image and translates it to the
    center of the image.

    :param img_: cv2/np.ndarray
    :param thresh: thresholding limit to determine CoG
    ---- Keyword only ----
    :param only_matrix: return just the transformation matrix
    """
    # TODO: should adapt for color
    img = img_.astype(np.float32)
    img /= img.max()
    img *= 255
    img = img.astype(np.uint8)
    img = cv2.medianBlur(img, 5)
    cent_y, cent_x = np.where(img > thresh)  # img.max())
    cent_y = cent_y.mean()
    cent_x = cent_x.mean()
    h, w = img.shape[:2]
    nc_y = (h / 2) - cent_y
    nc_x = (w / 2) - cent_x
    aff_mat = np.float32([
        [1, 0, nc_x],
        [0, 1, nc_y],
    ])
    if only_matrix:
        return aff_mat
    out = cv2.warpAffine(img_, aff_mat, (w, h))
    return out


def ecc_align(img1, img2, *,
        cvt_code=cv2.COLOR_BGR2GRAY,
        epsilon=1e-6,
        iters=100,
        interpolation=cv2.INTER_CUBIC,
        ecc_mask=None,
        gauss_size=5,
        ):
    """
    Performs ECC alignment of img2 over img1.

    :param img1: cv2/np.ndarray
    :param img2: cv2/np.ndarray
    ---- Keyword only ----
    :param cvt_code: cv2_COLOR_* familiy, cv2.COLOR_BGR2GRAY by default
    
    Also  the argument of cv2.findTransformECC:
        `epsilon`, `iters`, `interpolation`, `ecc_mask`, `gauss_size`
    """

    if cvt_code is not None:
        gray1 = cv2.cvtColor(img1, cvt_code)
        gray2 = cv2.cvtColor(img2, cvt_code)
    else:  # for chromatic correction we'll be passing channels individually
        gray1 = img1.copy()
        gray2 = img2.copy()
    criteria = (
        cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
        iters,
        epsilon
    )
    w, h = img1.shape[-2:][::-1]
    warp_mode = cv2.MOTION_HOMOGRAPHY
    warp_matrix = np.eye(3, 3, dtype=np.float32)
    g1, g2 = sobel(gray1), sobel(gray2)
    cc, warp_matrix = cv2.findTransformECC(
        g1, g2, warp_matrix, warp_mode,
        criteria, ecc_mask, gauss_size
    )
    warped = cv2.warpPerspective(img2, warp_matrix, (w, h),
        flags=interpolation + cv2.WARP_INVERSE_MAP
    )
    return warped
