# coding:utf-8

import requests
import time
import re
import os
import urllib
import json
import sys

stock_no = sys.argv[1]

GET_STOCK_ID_URL = "https://www.cmoney.tw/follow/channel/getdata/ChannelIdByStockId?stockId=" + stock_no

try:
    res = requests.get(GET_STOCK_ID_URL, timeout=5)
    channelID = res.json()

    GET_STOCK_INFO_URL = "https://www.cmoney.tw/follow/channel/getdata/GetStockOtherInfo?stockId=" + \
        stock_no + "&channelId=" + str(channelID)

    res = requests.get(GET_STOCK_INFO_URL, timeout=5)
    data = res.json()

    print(json.dumps({
        "stock_no": stock_no,
        "stock_name": data["StockInfo"]["Name"],
        "now_price": data["StockInfo"]["Price"],
        "now_amount": data["StockInfo"]["Quantity"],
        "now_diff": data["StockInfo"]["Change"],
        "now_percent": data["StockInfo"]["ChgPercent"]
    }))

except:
    print(json.dumps({
        "stock_no": stock_no,
        "stock_name": "-1",
        "now_price": "-1",
        "now_amount": "-1",
        "now_diff": "-1",
        "now_percent": "-1"
    }))
