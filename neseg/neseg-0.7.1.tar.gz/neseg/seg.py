import sys
import os
import xlrd
import ahocorasick

import neseg.lib.FMM as fmm
import neseg.lib.RMM as rmm

NESEG_VERSION='0.7'

def readCSV2List(filePath):
    try:
        file=open(filePath,'r',encoding="utf-8")
        context = file.read() 
        list_result=context.split("\n")# 以回车符\n分割成单独的行
        
        length=len(list_result)
        for i in range(length):
            list_result[i] =list_result[i].split(",")
        return list_result
    except Exception as e:
        print("文件[%s]读取失败" % filePath, "异常: %s" % e,sep=',')
        return
    finally:
        file.close();# 操作完成一定要关闭

# 令牌分割
def dictTokenizer(sent,dict): 
    # 国名
    dictWords = []
    while True:
        strm = fmm.cut_words(sent,dict,'')
        dictWords = dictWords + strm
        strmlen = len(''.join(strm))
        #print("While country:",sentence,"strm:",''.join(strm),"strmlen:",strmlen)
        sent = sent[strmlen:]
        if strmlen <=1 :
            break
    return (''.join(dictWords), sent)

def segbydict(ne,dcountry,dprovince,dcity,dcounty,dsuffix):
    dicCountry = fmm.load_dic(dcountry) 
    dicProvince = fmm.load_dic(dprovince) 
    dicCity = fmm.load_dic(dcity)
    dicCounty = fmm.load_dic(dcounty) 

    token1, st1 = dictTokenizer(ne,dicCountry)
    token2, st2 = dictTokenizer(st1,dicProvince)
    token3, st3 = dictTokenizer(st2,dicCity)
    token4, st4 = dictTokenizer(st3,dicCounty)

    lst1 = readCSV2List(dsuffix)
    lst_suffix = [row[0] for row in lst1]

    token5 = rmm.cut_words(st4, lst_suffix)
    st5 = st4.rstrip(''.join(token5))

    strtemp = ','.join([token1,token2,token3,token4,st5,','.join(token5)])
    return strtemp
