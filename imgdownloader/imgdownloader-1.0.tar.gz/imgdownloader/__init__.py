import cv2
import numpy as np
import urllib.request

def download(url,path):
    """The image in the above URl will be downloaded to the path.\nPath should include name\nex : C/User/pc/Desktop/img.png"""
    imglink=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imglink.read()))
    img = cv2.imdecode(imgNp,-1)
    cv2.imwrite(path,img)
