from server.data_get_save import get_data

from server.eAd import paillier

def align1(public_key):
    # 通过公钥进行加密



    sample_key = get_data.get_data_key()
    sample_encrypted = paillier.encrypt_all(public_key,sample_key)
    sample_encrypted_rand = paillier.add_rand(sample_encrypted)

    return sample_encrypted_rand