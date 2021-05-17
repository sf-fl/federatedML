
import pandas as pd

import numpy as np


from sklearn.tree import DecisionTreeClassifier


def _optimal_binning_boundary(x: pd.Series, y: pd.Series, nan: float = -999.) -> list:
    """
        利用决策树获得最优分箱的边界值列表
    """

    boundary = []  # 待return的分箱边界值列表
    x = x.fillna(nan).values  # 填充缺失值
    y = y.values
    clf = DecisionTreeClassifier(criterion='gini',  # “基尼系数”最小化准则划分
                                 max_leaf_nodes=10,  # 最大叶子节点数
                                 min_samples_leaf=0.05)  # 叶子节点样本数量最小占比
    clf.fit(x.reshape(-1, 1), y)  # 训练决策树
    n_nodes = clf.tree_.node_count
    children_left = clf.tree_.children_left
    children_right = clf.tree_.children_right
    threshold = clf.tree_.threshold
    for i in range(n_nodes):
        if children_left[i] != children_right[i]:  # 获得决策树节点上的划分边界值
            boundary.append(threshold[i])
    boundary.sort()
    min_x = x.min()
    max_x = x.max() + 0.1  # +0.1是为了考虑后续groupby操作时，能包含特征最大值的样本
    boundary = [min_x] + boundary + [max_x]
    return boundary


def feature_woe_iv(x: pd.DataFrame, con_list: list, discon_list: list, y: pd.Series, nan: float = -999.) -> pd.DataFrame:
    """
        计算变量各个分箱的WOE、IV值，返回一个DataFrame
    """

    if x.isnull:
        x.fillna(nan)
    all_iv_detail = pd.DataFrame([])

    for col in con_list:
        print(x[col])
        boundary = _optimal_binning_boundary(x[col], y, nan)  # 获得最优分箱边界值列表
        df = pd.concat([x[col], y], axis=1)
        df.columns = ['x', 'y']  # 特征变量、目标变量字段的重命名
        df['bins'] = pd.cut(x=x[col], bins=boundary, right=False)  # 获得每个x值所在的分箱区间
        grouped = df.groupby('bins')['y']  # 统计各分箱区间的好、坏、总客户数量
        result_df = grouped.agg([('good', lambda y: (y == 0).sum()),
                                 ('bad', lambda y: (y == 1).sum()),
                                 ('total', 'count')])
        print(result_df)
        result_df['rank'] = range(len(grouped))
        result_df['good_pct'] = result_df['good'] / result_df['good'].sum()  # 好客户占比
        result_df['bad_pct'] = result_df['bad'] / result_df['bad'].sum()  # 坏客户占比
        result_df['total_pct'] = result_df['total'] / result_df['total'].sum()  # 总客户占比
        result_df['badrate'] = result_df['bad'] / result_df['total']  # 坏比率
        result_df['woe'] = np.log(result_df['bad_pct'] / result_df['good_pct'])  # WOE
        result_df['badcumsum'] = result_df['bad'].cumsum()
        result_df['goodcumsum'] = result_df['good'].cumsum()
        result_df['ks'] = max(result_df['badcumsum'] / sum(result_df['badcumsum']) - result_df['goodcumsum'] / sum(
           result_df['goodcumsum']))
        result_df['iv'] = (result_df['bad_pct'] - result_df['good_pct']) * result_df['woe']  # IV
        result_df['IV'] = result_df['iv'].sum()
        result_df['var_name'] = x[col].name
        result_df.reset_index(inplace=True)
        print(f"该变量IV = {result_df['iv'].sum()}")
        all_iv_detail = pd.concat([all_iv_detail, result_df], axis=0)
        print(all_iv_detail)

    for col in discon_list:
        print(x[col])
        temp = x[col].copy().drop_duplicates().tolist()
        temp.sort()
        temp.append(temp[-1]+0.1)
        print(temp)
        boundary = temp  # 获得最优分箱边界值列表
        df = pd.concat([x[col], y], axis=1)
        df.columns = ['x', 'y']  # 特征变量、目标变量字段的重命名
        df['bins'] = pd.cut(x=x[col], bins=boundary, right=False)  # 获得每个x值所在的分箱区间
        grouped = df.groupby('bins')['y']  # 统计各分箱区间的好、坏、总客户数量
        result_df = grouped.agg([('good', lambda y: (y == 0).sum()),
                                 ('bad', lambda y: (y == 1).sum()),
                                 ('total', 'count')])
        print(result_df)
        result_df['rank'] = range(len(grouped))
        result_df['good_pct'] = result_df['good'] / result_df['good'].sum()  # 好客户占比
        result_df['bad_pct'] = result_df['bad'] / result_df['bad'].sum()  # 坏客户占比
        result_df['total_pct'] = result_df['total'] / result_df['total'].sum()  # 总客户占比
        result_df['badrate'] = result_df['bad'] / result_df['total']  # 坏比率
        result_df['woe'] = np.log(result_df['bad_pct'] / result_df['good_pct'])  # WOE
        result_df['badcumsum'] = result_df['bad'].cumsum()
        result_df['goodcumsum'] = result_df['good'].cumsum()
        result_df['ks'] = max(result_df['badcumsum'] / sum(result_df['badcumsum']) - result_df['goodcumsum'] / sum(
            result_df['goodcumsum']))
        result_df['iv'] = (result_df['bad_pct'] - result_df['good_pct']) * result_df['woe']  # IV
        result_df['IV'] = result_df['iv'].sum()
        result_df['var_name'] = x[col].name
        result_df.reset_index(inplace=True)
        print(f"该变量IV = {result_df['iv'].sum()}")
        all_iv_detail = pd.concat([all_iv_detail, result_df], axis=0)
        print(all_iv_detail)
    return all_iv_detail


data = pd.read_table('final_数据.csv',encoding='GBK',sep=",")

print(data)
print(data["Y"])
print(data.iloc[:,0:-1])
y = data["Y"]
x = data.iloc[:,0:-1]
# print(np.isnan(x).any())
x_list = x.columns.values.tolist()
x_con = ['年龄','居住时间', '工作时间', '税后年薪', '放款金额', '首付金额', '客户利率', '实际利率', '抵押逾期天数','合同期数']
x_discon = ['客户性别','申贷次数','学历','星座','婚姻状况','户籍省份',	'户籍城市',	'居住地省份',	'居住地城市','户籍居住地一致性','居住顶房产性质','工作职务代码','工作职称',
            '职业行业代码','驾驶证','房产','神速贷','经销商省份','经销商城市','与居住城市','与户籍城市','与居住省份','据户籍省份','经销商代码','单位行业代码']
for i in range(len(x_con)-1, -1, -1):
    if x_con[i] not in x_list:
        x_con.pop(i)
for i in range(len(x_discon)-1, -1, -1):
    if x_discon[i] not in x_list:
        x_discon.pop(i)

woe = feature_woe_iv(x, x_list, [], y)
bon_list = woe["bins"]
woe_list = list(woe['woe'])
# woe.to_excel(r'1.xls',sheet_name='Sheet1')  #数据输出至Excel

with open('5月final.txt', 'a', encoding='GBK') as f2:
    with open('5月预处理.txt', 'r', encoding='GBK') as f1:
        f2.write(f1.readline())
        # f1.readline()
        l = f1.readline().strip().split()
        x_tag = ['年龄','居住时间', '户籍居住地一致性', '单位行业代码',  '税后年薪',
                 '客户利率', '实际利率', '经销商代码', '申贷次数', '与居住城市']
        temp = {'Y': {}, '评分': {}}
        xishu = {'客户性别': 0.61573684, '学历': 0.72163206, '婚姻状况': 1.0052314, '居住顶房产性质': 0.49866245,
                 '单位行业代码': 0.73429126, '驾驶证': 0.7104414, '税后年薪': 0.5359129,
                 '合同期数': 0.72520469, '放款金额': 0.58368941, '首付金额': 0.57555303, '实际利率': 0.32558667,
                 '经销商代码': 0.8128351, '申贷次数': 0.91957113}
        count = 0
        tt = []
        ff = []
        limit = {}
        flag = 0
        # score = 103 + 0.00581218 * (-11.7)
        for i, tag in enumerate(x_list):
            sasd = woe[woe.var_name == tag]
            for j in range(len(sasd)):
                ccc = sasd.loc[j, 'bins']
                a = str(ccc).strip('[').strip(')').split(',')
                if j == 0:
                    limit[tag] = {}
                    temp[tag] = {}
                    limit[tag][0] = float(a[0])
                if j == len(sasd) - 1:
                    limit[tag][1] = float(a[1])
        while l:
            for i,tag in enumerate(x_list):
                sasd = woe[woe.var_name == tag]
                cc = float(l[i])
                flag = 0
                for j in range(len(sasd)):
                    ccc = sasd.loc[j, 'bins']
                    if cc in ccc:
                        # temp[tag][count] = j+1
                        # score += xishu[tag] * sasd.loc[j, 'woe'] * (-11.7)
                        tt.append(str(sasd.loc[j, 'woe']))
                        flag = 1
                        break
                if flag != 1:
                    if cc < limit[tag][0]:
                        # temp[tag][count] = 1
                        # score += xishu[tag] * sasd.loc[j, 'woe'] * (-11.7)
                        tt.append(str(sasd.loc[0, 'woe']))
                        continue
                    if cc >= limit[tag][1]:
                        # temp[tag][count] = len(sasd)
                        # score += xishu[tag] * sasd.loc[j, 'woe'] * (-11.7)
                        tt.append(str(sasd.loc[len(sasd) - 1, 'woe']))
                        continue
            # temp['Y'][count] = l[-1]
            # temp['评分'][count] = score
            # score=103+0.00581218*(-11.7)
            tt.append(str(l[-1]))
            f2.write(' '.join(tt) + '\n')
            tt =[]
            l = f1.readline().strip().split()
            count += 1
            if count % 1000 == 0:
                print('%d个啦' % count)
data = pd.DataFrame(temp)
