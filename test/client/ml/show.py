#! -*- coding=utf-8 -*-
import pylab as pl
from math import log, exp, sqrt
from sklearn.metrics import roc_curve, auc
from sklearn.datasets import load_breast_cancer
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

cancer = load_breast_cancer()
x = pd.DataFrame(load_breast_cancer().data)
y = pd.DataFrame(load_breast_cancer().target)
x['tt'] = 1
y['tt'] = 1
data = pd.merge(x,y,on='tt')
data.to_csv('data.csv')
result = pd.read_csv('%s/result.csv' % os.path.dirname(os.getcwd()))
y_pred = result['p'].tolist()
y_true = result['y'].apply(lambda x : int(x)).to_list()


# Compute ROC curve and ROC area for each class
fpr,tpr,threshold = roc_curve(y_true, y_pred) ###计算真正率和假正率
roc_auc = auc(fpr,tpr) ###计算auc的值




plt.figure(figsize=(10, 10))
plt.plot(fpr, tpr, color='darkorange',
     lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example(test)')
plt.legend(loc="lower right")
plt.savefig("ROC(test).png")
plt.show()
plt.plot(tpr,lw=2, label='tpr')
plt.plot(fpr,lw=2, label='fpr')
plt.plot(tpr - fpr, label = 'ks')
plt.title('KS = %0.2f(test)' % max(tpr-fpr))
plt.legend(loc="lower right")
plt.savefig("KS(test).png")
plt.show()