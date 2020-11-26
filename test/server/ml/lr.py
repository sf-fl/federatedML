import math

from server.federation import alignment
from server.eAd import paillier
import pandas as pd
import numpy as np
import rsa


global theta
theta = pd.Series(np.zeros(0))  # 设置权重参数的初始值
rsa_len = 1112


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


def lr1(ub_list,ppk_b):
    x_a = alignment.x
    rpk_a, rsk_a = rsa.newkeys(rsa_len)
    n = alignment.x.shape[1]  # 特征个数
    global theta
    theta = pd.Series(np.zeros(n))
    u_list = []
    for i in range(x_a.shape[0]):
        xa = x_a.iloc[i]
        ub = ub_list[i]
        ua = cal_ua(xa,theta)
        ua = int(paillier.encipher(ua,ppk_b))
        u = paillier.plus(ua,ub,ppk_b)
        u_code = int2bytes(u, rsa_len//8-11)
        u = rsa.encrypt(u_code, rpk_a)
        u = bytes2int(u)
        u_list.append(u)

    return [[rpk_a.n,rpk_a.e], u_list]