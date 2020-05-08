
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import nltk
import os
def Hello():
    return "Hola"

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def createList():

    wordsAdded = []
    cwd = os.getcwd()
    os.chdir(a)
    fileList = os.listdir(os.getcwd())

def clean_title(title):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ',',
    '!', '&', ';', '@', '#', '$', '%', '^', '(', ')', '-', '_', '~', '+', '=',
    '[', ']', '{', '}']
    for c in invalid_chars:
        title = title.replace(c, '')
    return title
import lxml.html as lh
from lxml.html.clean import clean_html

def lxml_to_text(html):
    doc = lh.fromstring(html)
    doc = clean_html(doc)
    return doc.text_content()

#Get the folder full of html pages and a path for the output with the InvertedIndexFreq revealed
#'C:/Users/pages/', 'C:/Users/output/'
def InvertedIndexFreqHelper(a,b):
    entries = os.listdir(a)

    print("***")
    print(str(a) + str(entries[1]))
    print("***")




    for i in range(len(entries)):
        name = str(entries[i])
        tmpFile = a + str(entries[i])
        print(tmpFile)
        HtmlFile = open(tmpFile, 'r', encoding='utf-8')
        PureHtml = HtmlFile.read()
        text = lxml_to_text(PureHtml)

        sent = []
        sentences = 0
        finalList = []
        tmp = []

        text = clean_title(text)
        tokens = nltk.word_tokenize(text)

        for word in tokens:
            if(word != "."):
                sent.append(word)
            if(word == "."):
                sentences += 1
                counts = dict()
                for word in sent:
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1
                tmp.append(counts)
                tmp.append(sentences)
                sent=[]

        for i in range(len( tmp)-1):

             if(i %2 ==0):
                for k, v in tmp[i].items():
                    finalList.append(k)
                    finalList.append(v)
                    finalList.append(tmp[i+1])

        finalDict = {}
        for i in range(len(finalList)):
            if(i%3==0):
                if (finalList[i] not in finalDict):
                    tmp = "(" + str(finalList[i+2]) + ":" + str(finalList[i+1]) + ")"
                    finalDict[finalList[i]]= [tmp]
                else:
                    tmp = "(" + str(finalList[i+2]) + ":" + str(finalList[i+1]) + ")"
                    finalDict[finalList[i]].append(tmp)
        Fin =[]
        for key, val in finalDict.items():
            tmp = str(key) + ":" + str(val)
            Fin.append(tmp)

    f = open(str(b)+ name+".txt","w", encoding="utf-8")
    i = 1
    for url in Fin:
        f.write(url)
        i += 1
        f.write('\n')
    f.close()
