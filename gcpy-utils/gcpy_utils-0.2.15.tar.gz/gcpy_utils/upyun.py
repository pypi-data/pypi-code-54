#coding:utf-8
# write  by  zhou
import datetime
import base64
import redis
import sys
import requests

_app = None
_redis_conn = redis.Redis('192.168.14.40',6379,6)


def up_to_upyun(key,content):
    '''上传图片到又拍云
    参数说明：
    key      保存到又拍云的路径 比如 /test/my.jpg
    content  文件的内容
    返回值：
    返回一个路径：
    比如：//imgse.cn.gcimg.net/test/my.jpg
    '''
    key = str(key)
    gmt = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    gmt = str(gmt)
    headers = {
        "Date", gmt,
        'Authorization', 'Basic %s' % (str(base64.b64encode(":".join(_redis_conn.get("upyun-config")
                                                                     .split("|"))))),
        "Content-Length", '%s' % len(content)
    }
    requests.post("https://v0.api.upyun.com/gcseoimg%s"%key, data=content, headers=headers)
    return "//imgse.cn.gcimg.net" + key