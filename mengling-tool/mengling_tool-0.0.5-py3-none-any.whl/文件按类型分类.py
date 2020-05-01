import os, shutil, copy
import easygui
import time
import os

path = r'F:\downFiles\kk显\Public_Files'  # 有空格需要注意格式


# 查看类型
def chakan():
    s = set()
    for root, dirs, files in os.walk(path):
        print(root)
        for file in files:
            s.add(file.split('.')[-1])
    for name in s:
        print(".", name)


def rename():
    # 规范格式
    y_path = path
    if path.find(' ') != -1:
        y_path = path.replace(' ', '" "')
    main = 'D:\\vs2019\\工程\\随机名字\\随机名字\\bin\\Debug\\随机名字.exe ' + y_path  # 以空格分界
    # 需要exe文件中在Main(string[] args)函数对args进行处理，实现直接调用
    os.system(main)  # 程序返回值，如正常结束则为0


filelist = []


def fen(new_path=path, *gslist):
    rename()  # 先处理随机名字，退出后进行下一步
    fen1(path)
    # 有选择筛选
    if len(gslist) > 0:
        for i in gslist:
            gs = new_path + "\\" + str(i)  # 获取格式文件夹路径
            if not os.path.isdir(gs):
                os.makedirs(gs)  # 新建文件目录
        for file in filelist:
            # 获取文件格式，并统一处理为小写，因为文件夹名字大小写不敏感
            g = str(file[1]).split('.')[-1].swapcase()
            if g in gslist:
                shutil.move(file[0] + "\\" + file[1], new_path + "\\" + g + "\\" + file[1])  # 移动文件
    # 按类型分类
    else:
        for file in filelist:
            gs = new_path + "\\" + str(file[1]).split('.')[-1]  # 获取格式文件夹路径
            if not os.path.isdir(gs):
                os.makedirs(gs)  # 新建文件目录
            shutil.move(file[0] + "\\" + file[1], gs + "\\" + file[1])  # 移动文件


def fen1(path1):
    for root, dirs, files in os.walk(path1):
        for file in files:
            for dir in dirs:
                fen1(dir)
            filelist.append([root, file])


# chakan()
# 格式统一为小写
# fen()
