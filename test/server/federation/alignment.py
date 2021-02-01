from server.io import get_data
import pandas as pd
from server.eAd import hash
from server.eAd import paillier
from server.federation import feature_engineering

global x
x = pd.DataFrame([])

def align1(public_key):
    # 通过公钥进行加密

    _,sample_key = get_data.get_data_key()
    sample_encrypted = paillier.encrypt_all(public_key,sample_key)
    sample_encrypted_rand = paillier.add_rand(sample_encrypted)

    return sample_encrypted_rand


def align2(b_key,id,key):
    b_key_series = pd.Series(b_key)
    dict_b = {'num_b':b_key_series.index,'hash':b_key_series.values}
    df_b_key = pd.DataFrame(dict_b)

    sample = get_data.get_data(id)
    a_key = sample[key]
    a_key_series = hash.ser2hash(a_key)
    dict_a = {'num_a': a_key_series.index, 'hash': a_key_series.values}
    df_a_key = pd.DataFrame(dict_a)

    result = pd.merge(df_a_key,df_b_key,on='hash',how='inner')

    result_num = result['num_a']
    index = ['%d' % i for i in result_num]
    result_sample = sample.iloc[index]
    result_sample = result_sample.reset_index(drop=True)
    global x
    x = result_sample.iloc[:, [1,-1]]
    x = feature_engineering.feating(x)

    return result['num_b']