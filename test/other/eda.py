import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys


os.chdir(os.path.dirname(sys.path[0]))

train = pd.read_csv('./client/data_storage/data_7.csv')
train.drop('phone_num', axis=1, inplace=True)
cols = [c for c in train.columns]   #返回数据的列名到列表里

print('Number of features: {}'.format(len(cols)))

print('Feature types:')
train[cols].dtypes.value_counts()

counts = [[], [], []]
for c in cols:
    typ = train[c].dtype
    uniq = len(np.unique(train[c]))          #利用np的unique函数看看该列一共有几个不同的数值
    if uniq == 1:                                       #  uniq==1说明该列只有一个数值
        counts[0].append(c)
    elif uniq == 2 and typ == np.int64:   #  uniq==2说明该列有两个数值，往往就是0与1的二类数值
        counts[1].append(c)
    else:
        counts[2].append(c)

print('Constant features: {}\n Binary features: {} \nCategorical features: {}\n'.format(*[len(c) for c in counts]))

print('Constant features:', counts[0])
print('Categorical features:', counts[2])

pal = sns.color_palette()

for c in counts[2]:
    value_counts = train[c].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title('Categorical feature {} - Cardinality {}'.format(c, len(np.unique(train[c]))))
    plt.xlabel('Feature value')
    plt.ylabel('Occurences')
    plt.bar(range(len(value_counts)), value_counts.values, color=pal[1])
    ax.set_xticks(range(len(value_counts)))
    ax.set_xticklabels(value_counts.index, rotation='vertical')
    plt.show()