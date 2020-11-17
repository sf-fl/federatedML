from data_get_save import get_data
from proxy import client_proxy
from eAd import paillier


def align():
    # 生成所需公钥、密钥
    key = paillier.Paillier()

    # 发送公钥并接收加密样本key
    x2_encry = client_proxy.align_1(key.get_public_key())

    # 处理样本
    sample,sample_key = get_data.get_data_key()
    sample_encrypted = key.encrypt_all(sample_key)

    # 发送加密后样本key并接收对齐结果
    num = client_proxy.align_2(sample_encrypted)

    return sample[num]

