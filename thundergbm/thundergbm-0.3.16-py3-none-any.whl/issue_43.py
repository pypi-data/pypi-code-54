import numpy as np
import pandas as pd
from thundergbm import TGBMClassifier
from thundergbm import TGBMRegressor

x1 = np.random.random((40, 2))
y1 = np.random.randint(0, 2, 40)

print(x1.shape)
print(y1.shape)

# clf = TGBMClassifier(verbose=1)
# clf.fit(x1, y1)
x2 = x1[3,:]
print(x2.shape)

print(x1[0:5])
print(x2)
x2 = [[0.16160398,0.6084721], ]
x2 = np.asarray(x2)
print(x2.shape)
clf = TGBMClassifier(n_trees=3, verbose=1)
# clf = TGBMRegressor()
clf.fit(x1, y1)
print(clf)
clf.predict(x2)
