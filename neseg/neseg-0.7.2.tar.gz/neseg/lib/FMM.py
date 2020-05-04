import ahocorasick

################ 正向分词词典加载 ######################
def load_dic(dicfile):
    from math import log
    dic = ahocorasick.Automaton()
    total = 0.0
    with open(dicfile,'r',encoding='UTF-8') as dicfile:
        dicwords = []
        for line in dicfile:
            line = line.split(',')
            dicwords.append((line[0], int(line[1])))
            total += int(line[1])    
    for i,j in dicwords:
        dic.add_word(i, (i, log(j/total))) #这里使用了对数概率，防止溢出
    dic.make_automaton()
    return dic

# 正向最大长度词典匹配切词
def cut_words(pST,dic,suffix=''):
    sent = pST
    words = ['']
    j = 0
    for i in sent:
        #i = i.encode('utf-8')
        if dic.match(suffix+words[-1] + i):
            words[-1] += i
        else:
            #words.append(i)
            j = j+1
            break
    if dic.exists(''.join(words)):
        #print("keys:",''.join(words))
        return words
    else:
        return []