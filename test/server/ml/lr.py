import math

from server.federation import alignment
from server.eAd import paillier
import pandas as pd
import numpy as np
import rsa


global theta
theta = pd.Series(np.zeros(0))  # 设置权重参数的初始值
rsa_len = 1112
ppk_a, psk_a = paillier.gen_key()


def cal_ua(x,theta):
    temp1 = np.dot(theta.T, x)
    return temp1


def bytes2int(raw_bytes: bytes) -> int:
    r"""Converts a list of bytes or an 8-bit string to an integer.

    When using unicode strings, encode it to some encoding like UTF8 first.

    >>> (((128 * 256) + 64) * 256) + 15
    8405007
    >>> bytes2int(b'\x80@\x0f')
    8405007

    """
    return int.from_bytes(raw_bytes, 'big', signed=False)


def int2bytes(number: int, fill_size: int = 0) -> bytes:
    """
    Convert an unsigned integer to bytes (big-endian)::

    Does not preserve leading zeros if you don't specify a fill size.

    :param number:
        Integer value
    :param fill_size:
        If the optional fill size is given the length of the resulting
        byte string is expected to be the fill size and will be padded
        with prefix zero bytes to satisfy that length.
    :returns:
        Raw bytes (base-256 representation).
    :raises:
        ``OverflowError`` when fill_size is given and the number takes up more
        bytes than fit into the block. This requires the ``overflow``
        argument to this function to be set to ``False`` otherwise, no
        error will be raised.
    """

    if number < 0:
        raise ValueError("Number must be an unsigned integer: %d" % number)

    bytes_required = max(1, math.ceil(number.bit_length() / 8))

    if fill_size > 0:
        return number.to_bytes(fill_size, 'big')

    return number.to_bytes(bytes_required, 'big')


def generate_random(n):
    return np.random.random_integers(0,1000000000,size=n)# todo


def lr1(ub_list,ppk_b):
    lamb = 1
    x_a = alignment.x
    n = alignment.x.shape[1]  # 特征个数
    global theta
    theta = pd.Series(np.zeros(n))

    ua_list = []
    gradA_pb = theta.apply(lambda x : int(paillier.encipher(lamb * 2 * pow(10,6) * x,ppk_b)))
    print(x_a.shape[0])
    for i in range(x_a.shape[0]):
        # 计算Uaa
        xa = x_a.iloc[i]
        ua = cal_ua(xa,theta)
        ua = int(paillier.encipher(ua,ppk_a))
        ua_list.append(ua)

        # 计算Grb
        ub = ub_list[i]
        u_pb = paillier.plus(ua,ub,ppk_b)
        u_pb_i = [paillier.multiply(u_pb,int((x[1]*1000)//1),ppk_b) for x in xa.items()]
        for num,ux in enumerate(u_pb_i):
            gradA_pb[num] = paillier.plus(ux,gradA_pb[num],ppk_b)
        if i % 100 == 0:
            print('%.f%%' % (i/x_a.shape[0]*100))
    ra = generate_random(n)
    ra_pb = [int(paillier.encipher(int(r),ppk_b)) for r in ra]
    for num,r in enumerate(ra_pb):
        gradA_pb[num] = paillier.plus(r, gradA_pb[num], ppk_b)
    gradA_pb = list(gradA_pb)
    return [gradA_pb, ua_list,ppk_a]

def lr2(gradB_pa, gradA_r):
    pass