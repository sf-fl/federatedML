import math

from server.federation import alignment
from server.eAd import paillier
import pandas as pd
import numpy as np
import time
import rsa


global theta_a,ra,alpha
# 设置权重参数的初始值
theta_a = None

rsa_len = 1112
ppk_a, psk_a = paillier.gen_key()
scal = 1000
alpha = 0.5

def cal_ua(x,theta):
    temp1 = np.dot(theta.T, x)
    return int(temp1)


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
    return np.trunc(np.random.rand(n)*(scal**3)*10+(scal**3))# todo


def lr1(ubb_list,ppk_b):
    lamb = 0.1
    x_a = alignment.x
    n = alignment.x.shape[1]  # 特征个数
    global theta_a
    if theta_a is None:
        theta_a = pd.Series(np.ones(n)*10)
    theta = theta_a.apply(lambda x: int(x * scal))
    uaa_list = []
    # gradA_pb = theta.apply(lambda x : int(paillier.encipher((-lamb * 2 * (scal ** 2) * x),ppk_b)))
    gradA_pb =  pd.Series(np.zeros(n)).apply(lambda x: int(paillier.encipher((-lamb * 2 * (scal ** 2) * x), ppk_b)))
    print(x_a.shape[0])
    time_start = time.time()
    for i in range(x_a.shape[0]):
        # 计算Uaa
        xa = x_a.iloc[i].apply(lambda x: int(x*scal))
        ua = cal_ua(xa,theta)
        uaa = int(paillier.encipher(ua,ppk_a))
        uaa_list.append(uaa)

        # 计算Uab
        uab = int(paillier.encipher(ua, ppk_b))

        # 计算Garb
        ubb = ubb_list[i]
        u_pb = paillier.plus(uab,ubb,ppk_b)
        u_pb_i = [paillier.multiply(u_pb,x,ppk_b) for x in xa]
        for num,ux in enumerate(u_pb_i):
            gradA_pb[num] = paillier.plus(ux,gradA_pb[num],ppk_b)
        if i % 1000 == 0:
            print('%.f%%' % (i/x_a.shape[0]*100))
    global ra
    ra = generate_random(n)
    ra_pb = [int(paillier.encipher(int(r),ppk_b)) for r in ra]
    for num,r in enumerate(ra_pb):
        gradA_pb[num] = paillier.plus(r, gradA_pb[num], ppk_b)
    gradA_pb = list(gradA_pb)
    print('uaa和garb的计算耗时：',time.time()-time_start)
    return [gradA_pb, uaa_list,ppk_a]

def lr2(gradB_pa, gradA_r):
    # 给B解密
    time_start = time.time()
    gradB_r = []
    for grad in gradB_pa:
        gradB_r.append(paillier.decipher(grad, ppk_a, psk_a))
    print('Gar解密耗时：', time.time() - time_start)

    x_a = alignment.x
    # gar消除随机数
    gradA = gradA_r - ra
    grad = gradA / 4 / (scal ** 3)/x_a.shape[0]
    print('当前梯度为',grad)
    global theta_a,alpha
    theta_a = theta_a - alpha * grad
    alpha *= 0.97
    print('学习率：', alpha)
    print('theta_a',theta_a)
    return gradB_r

def sigmoid(x):
    # TODO: Implement sigmoid function
    return 1/(1 + np.exp(-x))


def save(id):
    model = theta_a
    model.to_csv(r'./server/data_storage/model_%s.csv' % id)


def pre(ub_list):
    x_a = alignment.x
    global theta_a
    ua_list = []
    for i in range(x_a.shape[0]):
        # 计算Uaa
        xa = x_a.iloc[i]
        ua = np.dot(theta_a.T, xa)
        ua_list.append(ua)
    u_list = np.array(ua_list) + np.array(ub_list)
    pred = pd.Series(u_list).apply(lambda x: sigmoid(x))
    return pred.tolist()
