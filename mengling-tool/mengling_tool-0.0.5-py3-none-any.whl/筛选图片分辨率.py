from PIL import Image
import shutil
import os
import xlwt
path = r'D:\-\图库'
newpath = r"C:\Users\氵梦灵\Desktop\x"
for root, dirs, files in os.walk(path):
    for file in files:
        img = Image.open(path + "/" + file)
        w = img.width  # 图片的宽
        h = img.height  # 图片的高
        if w >= 1920 and h >= 1080 and w / h >= 0.8*192/108 and w / h <= 1.2*192/108:
            shutil.copyfile(path + "/" + file, newpath + "/" + file)  # 复制文件
if __name__=='__main__':

    #新建一个excel的表格
    f = xlwt.Workbook()
    #在新建的表格中创建一个叫‘python’的表
    sheet = f.add_sheet("python")
    sheet.write(0,0, "1列")
    sheet.write(0,1, "2列")
    #依次创建列名 第一个参数表示行 第二个参数表示列 第三个参数表示要填的名字
    sheet.write(0,2, "3列")
    sheet.write(0,3, "4列")
    sheet.write(0,4, "5列")
    # 保存名字为python,xls的excel表格
    f.save('python1.xls')