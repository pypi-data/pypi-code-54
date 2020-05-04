
### 反向切词###
def cut_words(sentence,word_dic):
    word_cut=[]
    max_length=max(len(word) for word in word_dic)
    words_length = len(sentence)
    cut_word_list=[]
    while words_length > 0:
        max_cut_length = min(words_length, max_length)
        for i in range(max_cut_length, 0, -1):
            new_word = sentence[words_length - i: words_length]
            if new_word in word_dic:
                cut_word_list.append(new_word)
                words_length = words_length - i
                break
            elif i == 1:
                #cut_word_list.append(new_word)
                words_length = words_length - 1
                break
    cut_word_list.reverse()
#    words=",".join(cut_word_list)
#    word_cut.append(words.lstrip("/"))
    return cut_word_list    
