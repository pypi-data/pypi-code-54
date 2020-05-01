import os, glob
import cv2
import numpy as np
from PIL import Image
# from arsocr.utils.extra.rectify import rectify
from wpkit.cv.table.rectify import rectify
from wpkit.cv import utils as cvutils
from wpkit.cv.utils import ImageSaver
imsaver=ImageSaver(save_dir=r'D:/data/work/超远/中转站/0430/results',remake_dir=False)
imsaver.deactive()
def save_to_dir(img,name=None):
    return imsaver.save(img,name)

def organize_points(box):
    '''
    clock-wise
    p0:lt,p1:rt,p2:rb,p4:lb
    :param box:
    :return:
    '''
    p0,p3, p1,p2 = sorted(box, key=lambda p: p[0])
    p03=[p0,p3]
    p12=[p1,p2]
    p0, p3 = sorted(p03, key=lambda p: p[1])
    p1, p2 = sorted(p12, key=lambda p: p[1])
    return box.__class__([p0,p1,p2,p3])
def crop_quad(img,box,size=None):
    p0, p1, p2, p3 = box
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = box
    w,h=((x1-x0+x2-x3)//2,(y3-y0+y2-y1)//2)
    w,h=int(w),int(h)
    w,h=size or (w,h)
    M=cv2.getPerspectiveTransform(np.float32([p0,p1,p3,p2]),np.float32([[0,0],[w,0],[0,h],[w,h]]))
    # print(img,M,w,h)
    img=cv2.warpPerspective(img,M,(w,h))
    return img
def get_table_contour(img,exclude_paper_edge_thresh=20):
    n=4
    # src = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img_blur=img
    img = cv2.bitwise_not(img)
    img_inverse=img
    save_to_dir(img)
    AdaptiveThreshold = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -2)
    # mask=AdaptiveThreshold
    mask = AdaptiveThreshold
    save_to_dir(mask)
    # contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contours = list(filter(lambda cont: cv2.contourArea(cont) > 30, contours))
    num = min(n, len(contours))
    contours = contours[:num]
    # 上面得到的contour可能是单个轮廓都是不完整的，但是叠加在一起有完整的，因此从第一次的contours  image中重新findContour
    blank=np.zeros_like(img_blur)
    img_contours=cv2.drawContours(blank,contours,-1,255,3)
    save_to_dir(img_contours)
    contours, hierarchy = cv2.findContours(img_contours, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contours = list(filter(lambda cont: cv2.contourArea(cont) > 30, contours))
    num = min(n, len(contours))
    contours = contours[:num]

    ones=np.ones_like(img_blur)
    thresh=exclude_paper_edge_thresh
    for i in range(len(contours)):
        mask=cv2.fillPoly(ones.copy(),[contours[i]],0)
        im=img_blur*mask
        mean=im.mean()
        if mean>thresh:
            return contours[i]
    if len(contours):
        return contours[0]
    return None
def get_table(img,max_approx_poly_distance=200,exclude_paper_edge_thresh=20):
    src_img=img.copy()
    contour=get_table_contour(img,exclude_paper_edge_thresh=exclude_paper_edge_thresh)
    if contour is None:
        return None
    im=cv2.drawContours(img.copy(),[contour],-1,[255,0,0],5)
    save_to_dir(im)
    approx=cv2.approxPolyDP(contour,max_approx_poly_distance,True)
    # print(approx.shape)

    if len(approx)==4:
        approx=[p[0] for p in approx]
        box=organize_points(approx)
        table=crop_quad(src_img,box)
    else:
        rect=cv2.boundingRect(approx)
        x1,y1,w,h=rect
        table=src_img[y1:y1+h,x1:x1+w]
    save_to_dir(table)
    return table
def cv_imread(f):
    from wpkit.cv.utils import cv2img
    return cv2img(Image.open(f))
def demo():
    # dir = '/home/ars/disk/chaoyuan/数据整理/ocr测试图片/exp/imgs'
    dir = r'D:/data/work/超远/中转站/0430/imgs'
    fs = glob.glob(dir + '/*.jpg')
    # fs=['']
    for i, f in enumerate(fs):
        assert os.path.exists(dir)
        assert os.path.exists(f)
        img = cv_imread(f)
        img=cvutils.transform.rescale(img,1)
        img = rectify(img)
        get_table(img)
if __name__ == '__main__':

    # corner()
    demo()

