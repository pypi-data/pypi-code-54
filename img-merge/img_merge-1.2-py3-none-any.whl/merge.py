import cv2
import os
import numpy as np
import sys

class Merge(object):
    def __init__(self,img_file,re_w = 256,re_h = 256,row = 3,column = 2):
        self.img_file = img_file
        self.re_w = re_w
        self.re_h = re_h
        self.row = row
        self.column = column
        self.imgs = [os.path.join(self.img_file,item) for item in os.listdir(self.img_file)]
        self.imgs.sort()
        print(f"img :{self.imgs}")
        print(f"img len:{self.imgs.__len__()}")
    def resize(self,img):
        return cv2.resize(img,(self.re_w,self.re_h))

    def run(self,row,column):
        if row and column:
            self.row = row
            self.column = column
        if self.imgs.__len__() == (self.row * self.column):
            self.out = np.zeros((self.re_w*self.column,self.re_h*self.row,3)).astype("uint8")
            #print(self.out.shape)
            for id, im_dir in enumerate(self.imgs):
                img = self.resize(cv2.imread(im_dir))
                xx,yy =id// self.column+1,id%self.column+1
                #print(xx,yy,img.shape,self.re_w,self.re_h)
                #print((yy-1)*self.re_h,yy*self.re_h-1,(xx-1)*self.re_w,xx*self.re_w-1)
                self.out[(yy-1)*self.re_h:yy*self.re_h,(xx-1)*self.re_w:xx*self.re_w,:] = img
            cv2.imwrite(f"{row}_{column}_merge.png",self.out)
            print("Done!")
            return 0
        else:
            return "Failure！"

if __name__ == "__main__":
    """use age"""
    if sys.argv.__len__() == 4:
        m = Merge(img_file= sys.argv[1])
        row = int(sys.argv[2])
        column = int(sys.argv[3])
        m.run(row,column)
    else:
        exit(0)

