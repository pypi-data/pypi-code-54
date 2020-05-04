# coding:utf-8

import pandas as pd
from sklearn.metrics import roc_auc_score,roc_curve,auc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV as gscv
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import glob
import math
import xgboost as xgb

from lapras.plot import bin_plot
from lapras.plot import badrate_plot

import lapras

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.display.max_colwidth = 100
pd.set_option('display.width',200)

'''
lapras项目主流程测试
'''

# if __name__ == '__main__':
#     pass
to_drop = []
df = pd.read_csv('data/test_data.csv',encoding="utf-8")
# print(lapras.detect(df))

# print(lapras.quality(df,target = 'bad'))

train_selected, dropped = lapras.selection.select(df.drop(to_drop,axis=1),target = 'bad', empty = 0.9, \
                                                iv = 0.02, corr = 0.9, return_drop=True, exclude=[])
# print(dropped)
# print(train_selected.shape)

c = lapras.transform.Combiner()
c.fit(train_selected, y = 'bad', method = 'dt', min_samples = 0.05,n_bins=5)
# c.load({'A': [0.6584, 0.747, 0.8757, 0.9306], 'C': [0.1577, 0.2077, 0.2517, 0.4534], \
#         'D': [0.5133, 0.695, 0.8326, 0.9369], 'F': [8.0279, 41.0498, 48.468, 54.1201],\
#         'G': [['nan'], ['良', 'u', '个', '去', '好', '我', '是', '看', '额'], ['优']]})
# print(c.export())

# print(c.transform(train_selected, labels=True).iloc[0:10, :])

# bin_plot(c.transform(train_selected[["A",'bad']], labels=False), x="A", target='bad')

# 转换为WOE值
transfer = lapras.transform.WOETransformer()
train_woe = transfer.fit_transform(c.transform(train_selected), train_selected['bad'], exclude=['bad'])
# print(train_woe)

# print(lapras.metrics.PSI(df['C'], df['D']))

# 将woe转化后的数据做逐步回归
final_data = lapras.selection.stepwise(train_woe,target = 'bad', estimator='ols', direction = 'both', criterion = 'aic', exclude = [])

# print(final_data.shape) # 逐步回归从31个变量中选出了10个
final_data = train_woe

# 用逻辑回归建模
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(solver='lbfgs')
lr.fit(final_data.drop(['bad'],axis=1), final_data['bad'])

# 预测训练
pred_train = lr.predict_proba(final_data.drop(['bad'],axis=1))[:,1]

from lapras.metrics import KS, AUC

print('train KS',KS(pred_train, final_data['bad']))
print('train AUC',AUC(pred_train, final_data['bad']))

card = lapras.ScoreCard(
    combiner = c,
    transer = transfer,
    class_weight = 'balanced',
    #C=0.1,
    base_score = 600,
    base_odds = 35 ,
    pdo = 60,
    rate = 2
)
col = list(final_data.drop(['bad'],axis=1).columns)
card.fit(final_data[col], final_data['bad'])
#输出标准评分卡
print(card.export())


