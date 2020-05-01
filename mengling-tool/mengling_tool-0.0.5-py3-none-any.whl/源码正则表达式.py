import requests
import urllib.request

url = "https://www.bilibili.com/video/av51214358?from=search&seid=14652254028759271069"


# 打开网页函数
def open_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


# 判断格式
def ifget(str):
    if str.find(".jpg") != -1 or str.find(".png") != -1:
        return True
    else:
        return False

if __name__=='__main__':

    strs = open_url(url).strip().split("\"")
    jpgs = set([s for s in strs if ifget(s)])
    # 筛选有效链接
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]
    for a in jpgs:
        try:
            opener.open(a)
            print(a)
        except:
            pass
