from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

def get_ind(data1, wordSet1, idfs1, matrix1):
    def transform(doca, wordSet, idfs):
        tf = {}
        ln_doc = len(doca)   
        sz = len(wordSet)
        matrix = csr_matrix((ln_doc, sz)).toarray()
        ind = 0itT
    
        for doc in doca:
            doc = doc.split(" ")
            ln = len(doc)
    
    
            for i in wordSet:
                tf[i] = 0
            for i in doc:
                tf[i] = 0    
            for i in doc:
                tf[i] = tf[i] + 1    
    
    
            for i in range(0, sz):
                matrix[ind][i] = (tf[wordSet[i]]/ln)*idfs[wordSet[i]]
            ind = ind + 1
        return matrix
    
    
    matrix2 = transform(data1, wordSet1, idfs1 )
    
    
    
    cos = cosine_similarity(matrix2, matrix1)
    cos = cos[0].tolist()
    ind = 0
    j = 0
    mx = cos[0]
    for i in cos:
        if mx<i:
            mx = i
            ind = j
        j = j+ 1
    return ind + 1


class Answer(object):
    def __init__(self, topic):
        self.topic = topic
        import pickle
        with open(topic+'_ans', 'rb') as p:
            self.ans = pickle.load(p)
    
    
    def get_ans(self,ans_no):
        import random
        rand_index = random.randint(0,len(self.ans[ans_no-1])-1)
        return self.ans[ans_no-1][rand_index]
