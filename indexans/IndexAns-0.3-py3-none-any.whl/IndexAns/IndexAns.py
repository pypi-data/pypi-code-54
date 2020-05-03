from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

def get_ind(data1, wordSet1, idfs1, matrix1, wordSet2, idfs2, matrix2):
    def transform(doca, wordSet, idfs):
        tf = {}
        ln_doc = len(doca)   
        sz = len(wordSet)
        matrix = csr_matrix((ln_doc, sz)).toarray()
        ind = 0
    
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
    
    
    matrix1_2 = transform(data1, wordSet1, idfs1 )
    matrix2_2 = transform(data1, wordSet2, idfs2 )
    
    
    
    cos1 = cosine_similarity(matrix1_2, matrix1)
    cos1 = cos1[0].tolist()
    ind = 0
    j = 0
    mx1 = cos1[0]
    for i in cos1:
        if mx1<i:
            mx1 = i
            ind = j
        j = j+ 1
    max_ind1 = ind + 1
    

    cos2 = cosine_similarity(matrix2_2, matrix2)
    cos2 = cos2[0].tolist()
    ind = 0
    j = 0
    mx2 = cos2[0]
    for i in cos2:
        if mx2<i:
            mx2 = i
            ind = j
        j = j+ 1
    max_ind2 = ind + 1

    if mx1>mx2:
        return max_ind1, 1
    else:
        return max_ind2, 2

    
    







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
