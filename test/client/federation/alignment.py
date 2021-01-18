from client.io import get_data
from client.proxy import client_proxy
from client.eAd import paillier
from client.eAd import hash


def align():
    # # 生成所需公钥、密钥
    # key = paillier.Paillier()
    #
    # # 发送公钥并接收加密样本key
    # x2_encrip = client_proxy.align_1(key.get_public_key())
    #
    # # 处理样本
    # sample,sample_key = get_data.get_data_key()
    # x2_encriped = key.encipher(x2_encrip)
    # sample_encriped = key.encipher(sample_key)

    sample, sample_key = get_data.get_data_key()
    sample_hash = hash.ser2hash(sample_key)

    # 发送加密后样本key并接收对齐结果
    num = client_proxy.align_2(sample_hash)
    index = ['%d' % i for i in num]
    result_sample = sample.iloc[index]
    result_sample = result_sample.reset_index(drop=True)
    x = result_sample.iloc[:,[1,-2]]
    y = result_sample.iloc[:,[-1,]]
    return x,y

