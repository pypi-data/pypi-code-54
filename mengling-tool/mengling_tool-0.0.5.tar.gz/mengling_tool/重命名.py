import os
if __name__=='__main__':

    path = r"C:\Users\氵梦灵\Desktop\森罗万象"
    for root, dirs, files in os.walk(path):
        for file in files:
            i = file.split('.flac')[0][-1]
            os.rename(path + "\\" + file, path + "\\" + "五维介质 - " + i + "-专辑.flac")  # 重命名文件
            # print(file)