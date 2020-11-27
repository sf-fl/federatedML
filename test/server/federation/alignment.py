from server.data_get_save import get_data
import pandas as pd
from server.eAd import hash
from server.eAd import paillier

global x
x = pd.DataFrame([])
global y
y = pd.DataFrame([])

def align1(public_key):
    # 通过公钥进行加密

    _,sample_key = get_data.get_data_key()
    sample_encrypted = paillier.encrypt_all(public_key,sample_key)
    sample_encrypted_rand = paillier.add_rand(sample_encrypted)

    return sample_encrypted_rand


def align2(b_key):
    b_key_series = pd.Series(b_key)
    dict_b = {'num_b':b_key_series.index,'hash':b_key_series.values}
    df_b_key = pd.DataFrame(dict_b)

    sample, a_key = get_data.get_data_key()
    a_key_series = hash.ser2hash(a_key)
    dict_a = {'num_a': a_key_series.index, 'hash': a_key_series.values}
    df_a_key = pd.DataFrame(dict_a)

    result = pd.merge(df_a_key,df_b_key,on='hash',how='inner')

    result_num = result['num_a']
    index = ['%d' % i for i in result_num]
    result_sample = sample.iloc[index]
    result_sample = result_sample.reset_index(drop=True)
    global x
    x = result_sample.iloc[:, [1, -2]]
    global y
    y = result_sample.iloc[:, [-1, ]]

    return result['num_b']