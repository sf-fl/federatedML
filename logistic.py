import numpy as np
import pandas as pd
import math
from pandasql import sqldf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

# 关联原始数据表格
education=pd.read_csv('D:\lbxx\data_education.csv')
marriage=pd.read_csv('D:\lbxx\data_marriage.csv')
asocciate=marriage
# associate=sqldf('''select t2.*,t1.income,t1.education from education t1 inner join marriage t2 on t1.phone_num=t2.phone_num''')
# 进行onehot
# values=np.array(associate['education'])
# integer_encoded=LabelEncoder().fit_transform(values)
# integer_encoded=integer_encoded.reshape(len(integer_encoded),1)
# onehot_encoded=OneHotEncoder(sparse=(False)).fit_transform(integer_encoded)
# inverted=LabelEncoder().inverse_transform([np.argmax(onehot_encoded[0,:])])
# 将原数据与其education的onehot编码关联起来
test=pd.get_dummies(associate)
# test=pd.concat([associate,onehot_encoded])
x=test.drop(columns=['phone_num','marriage']).values
y=test.iloc[:,3].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
sc=StandardScaler()
mms=MinMaxScaler()
sc.fit(x_train)
mms.fit(x_train)
x_train_std=sc.transform(x_train)
x_test_std=sc.transform(x_test)
x_train_mms=mms.transform(x_train)
x_test_mms=mms.transform(x_test)
lr=LogisticRegression(max_iter=10000,random_state=1)
lr.fit(x_train_std, y_train)
r = lr.score(x_train, y_train)
y_predict = lr.predict(x_test)
y_prob = lr.predict_proba(x_test)[:,1]
y_predict_ = lr.predict(x_train)
y_prob_ = lr.predict_proba(x_train)[:,1]


print('-----------------测试-----------------')
train_right_counts = 0
for i in range(x_train_std.shape[0]):
    original_val = y_train[i]
    predict_val = lr.predict(x_train_std[i,:].reshape(1, -1))
    if original_val == predict_val:
        train_right_counts += 1
print("训练集准确率：", ((train_right_counts * 1.0) / x_train_std.shape[0]))
test_right_counts = 0
for i in range(x_test_std.shape[0]):
    original_val = y_test[i]
    predict_val = lr.predict(x_test_std[i, :].reshape(1, -1))
    if original_val == predict_val:
        test_right_counts += 1
print("测试集准确率：", ((test_right_counts * 1.0) / x_test_std.shape[0]))

print(metrics.accuracy_score(y_train, y_predict_, normalize=True, sample_weight=None))
cfm = metrics.confusion_matrix(y_train, y_predict_, labels=None, sample_weight=None)
print(cfm)
print(metrics.classification_report(y_train, y_predict_, labels=None, sample_weight=None))

print(metrics.accuracy_score(y_test, y_predict, normalize=True, sample_weight=None))
cfm = metrics.confusion_matrix(y_test, y_predict, labels=None, sample_weight=None)
print(cfm)
print(metrics.classification_report(y_test, y_predict, labels=None, sample_weight=None))
row_sums = np.sum(cfm, axis=1)  # 求出混淆矩阵每一行的和
error_matrix = cfm / row_sums  # 求出每一行中每一个元素所占这一行的百分比
# 将矩阵中对角线上的元素都定位0
# np.fill_diagonal(error_matrix, 0)
plt.matshow(error_matrix, cmap=plt.cm.gray)
plt.show()
print("RMSE = ",math.sqrt(sum((y_test - y_prob) ** 2)/len(y_prob)))

fpr, tpr, thresholds = metrics.roc_curve(y_test, y_prob, pos_label=1)
fpr_, tpr_, thresholds_ = metrics.roc_curve(y_train, y_prob_, pos_label=1)

for i in range(tpr.shape[0]):
    if tpr[i] > 0.5:
        print(tpr[i], 1 - fpr[i], thresholds[i])
    break

# train
roc_auc_ = metrics.auc(fpr_, tpr_)
plt.figure(figsize=(10, 10))
plt.plot(fpr_, tpr_, color='darkorange',lw=2, label='ROC curve (area = %0.2f)' % roc_auc_)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example(train)')
plt.legend(loc="lower right")
plt.savefig("ROC（train）.png")
plt.show()
plt.plot(tpr_, lw=2, label='tpr')
plt.plot(fpr_, lw=2, label='fpr')
plt.plot(tpr_ - fpr_, label='ks')
plt.title('KS = %0.2f(train)' % max(tpr_ - fpr_))
plt.legend(loc="lower right")
plt.savefig("KS(train).png")
plt.show()

# test
roc_auc = metrics.auc(fpr, tpr)
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

# 绘制测试集结果验证
# test_validate(x_test=x_test, y_test=y_test, y_predict=y_predict, classifier=lr)
