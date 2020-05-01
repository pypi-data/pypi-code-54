import os
import shutil

path = r"C:\Users\氵梦灵\Documents\WeChat Files\ljh1321443305"
newpath = r"C:\Users\氵梦灵\Desktop\123"
newname = ".png"

def re(path):
    for root, dirs, files in os.walk(newpath):
        for file in files:
            os.rename(root + "\\" + file,root+ "\\" +newname)
        '''
        if file.find('.') == -1:
            shutil.copyfile(root + "\\" + file, newpath + "\\" + file + new)
        elif file.find('.gif') != -1:
            shutil.copyfile(root + "\\" + file, newpath + "\\" + file)
'''

re(path)