from data_get_save import get_data
from proxy import client_proxy

def align():
    # 生成所需公钥、密钥
    key = 0
    # 发送公钥
    client_proxy.align_1(key)

    sample = get_data.get_data_key()
    sample_encrypted = sample
    client_proxy.align_2(sample_encrypted)