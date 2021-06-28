import pandas as pd
import numpy as np
from client.eAd import paillier
from client.proxy import client_proxy


def woe_fed(x, ip, port, id):
    pass


def conti_binning(x, y, nan):
    return []


def disconti_binning(x, y, nan):
    temp = x.copy().drop_duplicates().tolist()
    temp.sort()
    temp.append(temp[-1] + 0.1)
    return []


def iv_detail(result_df,grouped):
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
    return result_df


def woe(x, y, method, id, ip, port):
    if method == 'local':
        x_all = list(x)
        all_iv_detail = pd.DataFrame()
        nan = -999.
        for col in x_all:
            if len(set(x[col])) > 5:
                boundary = conti_binning(x[col], y, nan)
            else:
                boundary = disconti_binning(x[col], y, nan)
            df = pd.concat([x[col], y], axis=1)
            df.columns = ['x', 'y']  # 特征变量、目标变量字段的重命名
            df['bins'] = pd.cut(x=x[col], bins=boundary, right=False)  # 获得每个x值所在的分箱区间
            grouped = df.groupby('bins')['y']  # 统计各分箱区间的好、坏、总客户数量
            result_df = grouped.agg([('good', lambda tt: (tt == 0).sum()),
                                     ('bad', lambda tt: (tt == 1).sum()),
                                     ('total', 'count')])
            result_df = iv_detail(result_df,grouped)
            result_df['var_name'] = x[col].name
            result_df.reset_index(inplace=True)
            print(f"该变量IV = {result_df['iv'].sum()}")
            all_iv_detail = pd.concat([all_iv_detail, result_df], axis=0)
            print(all_iv_detail)
    elif method == 'online':
        # 构建加密y和1-y
        # 生成key
        pk, sk = paillier.gen_key()
        y_encrypt = y.iloc[:, 0].apply(lambda tt: int(paillier.encipher(tt, pk)))
        y_r_encrypt = y.iloc[:, 0].apply(lambda tt: int(paillier.encipher(1-tt, pk)))
        result = client_proxy.woe_1(y_encrypt, y_r_encrypt, id, pk, ip, port)
        print(result)









