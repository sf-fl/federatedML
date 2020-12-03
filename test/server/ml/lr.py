import math

from server.federation import alignment
from server.eAd import paillier
import pandas as pd
import numpy as np
import time
import rsa


global theta_a,ra
# 设置权重参数的初始值


rsa_len = 1112
ppk_a, psk_a = paillier.gen_key()
scal = 100


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
    return np.random.random_integers((scal**3),(scal**3)*10,size=n)# todo


def lr1(ub_list,ppk_b):
    lamb = 1
    x_a = alignment.x
    n = alignment.x.shape[1]  # 特征个数
    global theta_a
    if theta_a is None:
        theta_a = pd.Series(np.zeros(n))
    theta = theta_a.apply(lambda x: int(x * scal))
    ua_list = []
    gradA_pb = theta.apply(lambda x : int(paillier.encipher(lamb * 2 * (scal ** 3) * x,ppk_b)))
    print(x_a.shape[0])
    time_start = time.time()
    for i in range(x_a.shape[0]):
        # 计算Uaa
        xa = x_a.iloc[i].apply(lambda x: int(x*scal))
        ua = cal_ua(xa,theta)
        ua = int(paillier.encipher(ua,ppk_a))
        ua_list.append(ua)

        # 计算Garb
        ub = ub_list[i]
        u_pb = paillier.plus(ua,ub,ppk_b)
        u_pb_i = [paillier.multiply(u_pb,x,ppk_b) for x in xa]
        for num,ux in enumerate(u_pb_i):
            gradA_pb[num] = paillier.plus(ux,gradA_pb[num],ppk_b)
        if i % 100 == 0:
            print('%.f%%' % (i/x_a.shape[0]*100))
    global ra
    ra = generate_random(n)
    ra_pb = [int(paillier.encipher(int(r),ppk_b)) for r in ra]
    for num,r in enumerate(ra_pb):
        gradA_pb[num] = paillier.plus(r, gradA_pb[num], ppk_b)
    gradA_pb = list(gradA_pb)
    print('uaa和garb的计算耗时：',time.time()-time_start)
    return [gradA_pb, ua_list,ppk_a]

def lr2(gradB_pa, gradA_r):
    # 给B解密
    time_start = time.time()
    gradB_r = []
    for grad in gradB_pa:
        gradB_r.append(paillier.decipher(grad, ppk_a, psk_a))
    print('Gar解密耗时：', time.time() - time_start)

    # gar消除随机数
    gradA = gradA_r - ra



    return gradB_r