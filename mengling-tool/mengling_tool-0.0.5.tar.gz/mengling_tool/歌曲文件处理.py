# -*- coding: utf-8 -*-

import os, shutil, copy

path_mp3 = "C:\\Users\\氵梦灵\\Desktop\\Music"
path_flat = "C:\\Users\氵梦灵\\Desktop\\new"
music_lei = ('MP3', 'mp3', 'Mp3', 'ape', 'wav', 'flac')


# old_将new放入old
def old_new(path_old, path_new, move=1):
    d_old, d_new = dict(), dict()
    # 建立文件名-文件全名的字典
    for root, dirs, files in os.walk(path_old):
        if root.find("Temp") != -1 or root.find("KugouMusic") != -1 or root.find("Cache") != -1: continue
        for file in files:
            if file.find("-") == -1 or file.find(".") == -1: continue
            d_old[file.split('.')[0]] = (root + "\\" + file)  # 当前路径下所有非目录子文件
    # 建立文件名-文件全名的字典
    for root, dirs, files in os.walk(path_new):
        if root.find("Temp") != -1 or root.find("KugouMusic") != -1 or root.find("Cache") != -1: continue
        for file in files:
            if file.find("-") == -1 or file.find(".") == -1: continue
            d_new[file.split('.')[0]] = (root + "\\" + file)  # 当前路径下所有非目录子文件
    # 将new放入old
    for new in d_new.keys():
        for old in d_old.keys():
            if new == old:
                print(d_old.get(new))
                os.remove(d_old.get(new))
                if move == 1:
                    # 需要保留原文件的扩展名
                    shutil.move(d_new.get(new), d_old.get(new).split('.')[0] + "." + d_new.get(new).split('.')[-1])
                else:
                    shutil.copyfile(d_new.get(new), d_old.get(new).split('.')[0] + "." + d_new.get(new).split('.')[-1])
                break


# 将目录下的文件进行格式化 V家 - 名.格式 不改动正确的格式
def zhuanji(path):
    arr = dict()
    for root, dirs, files in os.walk(path):
        for file in files:
            mp3 = root + "\\" + file
            if mp3.find('-') == -1 or mp3.split('-')[-1].find("专辑.") == -1:
                arr[mp3] = mp3  # 当前路径下所有非目录子文件
    # 将名字格式化
    for mp3 in arr.keys():
        # 移除非法数字
        if len(mp3.split('\\')[-1].split('.')) > 2:
            temp = mp3.split('.')[0]
            temp = temp.replace(temp.split('\\')[-1], "")
            temp += mp3.split('.')[1] + "." + mp3.split('.')[2]
            arr[mp3] = temp
        qian = arr[mp3].split(arr[mp3].split('\\')[-1])[0]
        hou = arr[mp3].split(qian)[-1]
        hou_new = "V家 - " + hou.split('.')[0].split(' - ')[-1] + "-专辑." + hou.split('.')[-1]
        arr[mp3] = qian + hou_new
    for key in arr.keys():
        shutil.move(key, arr[key])

    # file_name(path_mp3, path_flat)


# 查看所有文件的类型
def leixing(*paths):
    s = set()
    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                s.add(file.split('.')[-1])
    print(s)


# 寻找重复文件并取出
def chongfu(mp3path, flatpath, new_path):
    s_f = dict()
    s_m = dict()
    for root, dirs, files in os.walk(flatpath):
        for file in files:
            temp = fenduan(root, file)
            if temp == None or temp == -1: continue
            s_f[temp["歌名"]] = fenduan(root, file)
    for root, dirs, files in os.walk(mp3path):
        for file in files:
            temp = fenduan(root, file)
            if temp == None or temp == -1: continue
            s_m[temp["歌名"]] = fenduan(root, file)
    if not os.path.exists(new_path + "\\copy\\"): os.makedirs(new_path + "\\copy\\")
    if not os.path.exists(new_path + "\\move\\"): os.makedirs(new_path + "\\move\\")
    for fn in s_f.keys():
        s_temp = copy.copy(s_m)
        for mn in s_temp.keys():
            if fn.split('-')[0] == mn.split('-')[0]:
                # 复制flat，移动mp3
                print(s_f.get(fn)["全称"])
                print(s_m.get(mn)["全称"])
                shutil.copyfile(s_f.get(fn)["全称"], new_path + "\\copy\\" + s_f.get(fn)["全名"])
                shutil.move(s_m.get(mn)["全称"], new_path + "\\move\\" + s_m.get(mn)["全名"])
                s_m.pop(mn)


# 将文件全称进行分解
def fenduan(root, name):
    fen = dict()
    # 文件类型判断
    if name.split('.')[-1] not in music_lei:
        print("文件：" + root + "\\" + name + " 不在音乐文件类型" + str(music_lei))
        return None
    fen["路径"] = root + "\\"
    fen["歌手"] = name.split(" - ")[0]
    fen["间符"] = " - "
    fen["歌名"] = name.split(fen["歌手"] + " - ")[-1].split('.')[0]
    fen["后缀"] = "." + name.split('.')[-1]
    fen["全称"] = root + "\\" + name
    fen["歌手+歌名"] = fen["歌手"] + fen["间符"] + fen["歌名"]
    fen["全名"] = name
    if fen["路径"] + fen["歌手"] + fen["间符"] + fen["歌名"] + fen["后缀"] != fen["全称"] \
            or fen["歌手"].find(",") != -1 or fen["歌手"].find("，") != -1:
        print(fen["全称"] + " 文件格式有误！返回None")
        return -1
    return fen


# 遍历文件
def bianli(path, temp_path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if fenduan(root, file) == -1:
                if not os.path.exists(temp_path + "\\错误格式音乐文件\\"): os.makedirs(temp_path + "\\错误格式音乐文件\\")
                shutil.move(root + "\\" + file, temp_path + "\\错误格式音乐文件\\" + file)


# 格式修复
def re(path, ci=5):
    if ci <= 0: return None
    temps = [[], [], []]
    for root, dirs, files in os.walk(path):
        temps[0].append(root)
        temps[1].append(dirs)
        temps[2].append(files)
    for i in range(len(temps[0])):
        root = temps[0][i]
        dirs = temps[1][i]
        files = temps[2][i]
    for file in files:
        newname = file
        if fenduan(root, file) == -1:
            # 将-改为 -
            if newname.find('-') != -1 and newname.find(' - ') == -1: newname = newname.replace("-", " - ")
            # 没有歌手改为未知歌手
            if newname.find('-') == -1: newname = "未知歌手 - " + newname
            # 删除多余点改为_
            if len(newname.split('.')) > 2:
                newname = newname.split(newname.split('.')[-1])[0].replace(".", "_") + "." + newname.split('.')[-1]
            # 将,，改为、
            if newname.split(" - ")[0].find(",") != -1 or newname.split(" - ")[0].find("，") != -1:
                newname = newname.split(" - ")[0].replace(",", "、").replace("，", "、") + " - " + newname.split(" - ")[-1]
            if file != newname:
                shutil.move(root + "\\" + file, root + "\\" + newname)
    re(path, ci - 1)


# 将文件全部归总取最大值
def file_sum(path, new_path):
    dr = dict()
    for root, dirs, files in os.walk(path):
        for file in files:
            filelist = fenduan(root, file)
            if filelist == None or filelist == -1: continue
            if dr.get(filelist["歌手+歌名"]) == None or \
                    int(os.path.getsize(filelist["全称"])) < int(os.path.getsize(root + "\\" + file)):
                dr[filelist["歌手+歌名"]] = root + "\\" + file
    for name in dr.keys():
        print(dr.get(name))
        path_temp = new_path + dr.get(name).split(path)[-1].split(name)[0]
        if not os.path.exists(path_temp): os.makedirs(path_temp)
        shutil.copyfile(dr.get(name), new_path + dr.get(name).split(path)[-1])


# 将音乐按歌手+歌名进行升级,放在new下
def up(oldpath, newpath, new):
    dr = dict()
    for root, dirs, files in os.walk(oldpath):
        for file in files:
            filelist = fenduan(root, file)
            if filelist == None or filelist == -1: continue
            if dr.get(filelist["歌手+歌名"]) == None or \
                    int(os.path.getsize(filelist["全称"])) < int(os.path.getsize(root + "\\" + file)):
                dr[filelist["歌手+歌名"]] = root + "\\" + file
    for root, dirs, files in os.walk(newpath):
        for file in files:
            filelist = fenduan(root, file)
            if filelist == None or filelist == -1: continue
            if filelist["歌手+歌名"] in dr.keys() and \
                    int(os.path.getsize(filelist["全称"])) > int(os.path.getsize(dr[filelist["歌手+歌名"]])):
                dr[filelist["歌手+歌名"]] = filelist["全称"]
    for name in dr.keys():
        print(dr.get(name))
        path_temp = new + dr.get(name).split(oldpath)[-1].split(newpath)[-1].split(name)[0]
        if not os.path.exists(path_temp): os.makedirs(path_temp)
        shutil.copyfile(dr.get(name), new + dr.get(name).split(oldpath)[-1].split(newpath)[-1])


# chongfu("C:\\Users\\氵梦灵\\Desktop\\手机", "D:\\KwDownload\\专辑", "C:\\Users\\氵梦灵\\Desktop\\新建文件夹")
# old_new(path_mp3, path_flat,0)
if __name__=='__main__':
    leixing("D:\-\图库")
# zhuanji("D:\\KwDownload\\专辑")
# print(fenduan("F:\\333\\move","洛天依-如旧.mp3"))
# bianli("C:\\Users\\氵梦灵\Desktop\\手机", "C:\\Users\\氵梦灵\\Desktop\\新建文件夹")
# re("C:\\Users\\氵梦灵\\Desktop\\新建文件夹")
# file_sum("C:\\Users\\氵梦灵\\Desktop\\新建文件夹", "C:\\Users\\氵梦灵\\Desktop\\333")
# up("C:\\Users\\氵梦灵\\Desktop\\手机", "D:\\KwDownload\\song", "C:\\Users\\氵梦灵\\Desktop\\new")
