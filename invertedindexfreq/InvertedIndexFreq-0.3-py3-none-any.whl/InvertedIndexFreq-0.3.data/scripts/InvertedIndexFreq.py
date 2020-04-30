class InvertedIndexFreq:

    import nltk
    sent = []
    text = "One Dos. Dos Dos. Tres. Cuatro One Cuatro."
    tokens = nltk.word_tokenize(text)
    sentences = 0
    finalList = []
    tmp = []
    print("It should work")
    for word in tokens:
        if(word != "."):
            sent.append(word)
            #print(word, sentences)
        if(word == "."):
            sentences += 1
            counts = dict()
            for word in sent:
                #print(sentences)
                print(word)
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
                    #counts[word] = str(sentences)
            tmp.append(counts)
            tmp.append(sentences)
            sent=[]
            #del counts["One"]
            #counts ={}
            #counts.clear()
            #print(counts)
    print(tmp)



    for i in range(len (tmp)):
        if (i %2 ==0):
            for key,val in tmp[0].items():
                print (key, ":", val, tmp[i+1], "times")
        else:
            continue

     for i in range(len( tmp)-1):
        if(i %2 ==0):
            for k, v in tmp[i].items():
                print (k, v)
                finalList.append(k)
                finalList.append(v)
                finalList.append(tmp[i+1])
            #print(tmp[i])
            #print(tmp[i+1])


    finalDict = {}
    for i in range(len(finalList)):
        if(i%3==0):
            print(finalList[i], " :" , "[(", finalList[i+1], " -> ", finalList[i+2],")]")
            if (finalList[i] not in finalDict):
                tmp = "(" + str(finalList[i+2]) + ":" + str(finalList[i+1]) + ")"
                finalDict[finalList[i]]= [tmp]
            else:
                tmp = "(" + str(finalList[i+2]) + ":" + str(finalList[i+1]) + ")"
                finalDict[finalList[i]].append(tmp)


    print(finalDict)
    text = "One Dos. Dos Dos. Tres. Cuatro One Cuatro."
    print(text)
    print("** ** **")
    for key, val in finalDict.items():
        print (key, ":", val)






    def printHello():
        return "Hello"
