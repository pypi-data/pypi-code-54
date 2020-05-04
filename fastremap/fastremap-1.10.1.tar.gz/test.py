import fastremap
import numpy as np 
import time 

labels = np.random.randint(0, 512**3, size=(512,512,512))
labels[0,0,0] = 512**3 + 10

s = time.time()
fastremap.renumber(labels, in_place=True)
# uniq_fr, cts_fr = fastremap.unique_via_renumber(labels.flatten())
print(time.time() - s)