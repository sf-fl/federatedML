from client.data_get_save import get_data
from client.proxy import client_proxy
from client.eAd import paillier


def align():
    # 生成所需公钥、密钥
    key = paillier.Paillier()

    # 发送公钥并接收加密样本key
    x2_encrip = client_proxy.align_1(key.get_public_key())

    # 处理样本
    sample,sample_key = get_data.get_data_key()
    x2_encriped = key.encipher(x2_encrip)
    sample_encriped = key.encipher(sample_key)

    # 发送加密后样本key并接收对齐结果
    num = client_proxy.align_2(x2_encriped,sample_encriped)

    return sample[num]

