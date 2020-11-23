import math
import time
import numpy as np
import pandas as pd
import rsa
from client.eAd import paillier
from client.proxy import client_proxy

lamb = 1


def cal_ub(theta,x,y):
    temp1 = np.dot(theta.T, x)
    temp2 = 2 * pow(10,6) * y.iloc[0]
    return temp1 - temp2


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



def update_grad(theta_b,x_b,y_b):
    rsa_len = 1112

    # 生成 key_b 和 ub 并发出
    ppk_b, psk_b = paillier.gen_key()
    rpk_b, rsk_b = rsa.newkeys(rsa_len)
    ub_list = []
    for i in range(x_b.shape[0]):
        xb = x_b.iloc[i]
        yb = y_b.iloc[i]
        ub = cal_ub(theta_b,xb,yb)
        ub_code = int(paillier.encipher(ub,ppk_b))
        # ub_code = int2bytes(ub_code, rsa_len//8-11)
        # ub_code = str(rsa.encrypt(ub_code, rpk_b))
        ub_list.append(ub_code)
    rpk_a, u_list = client_proxy.learn_1(ub_list,ppk_b)
    for i in range(x_b.shape[0]):
        xb = x_b.iloc[i]
        u = u_list[i]
        uxb = paillier.multiply(u,xb[0],ppk_b)




def update_theta(grad, theta, alpha):
    theta = theta - alpha * 4 * pow(10,-9) * grad
    return theta


def logistic_regression(X, y):
    """
    逻辑回归算法
    :param X: mxn矩阵
    :param y: mx1矩阵
    :return: nx1矩阵
    """
    start = time.time()
    m = X.shape[0]  # 样本个数
    n = X.shape[1]  # 特征个数
    # y = y.reshape(m, 1)
    # cost_record = []  # 记录代价函数的值
    alpha = 0.1  # 学习率
    maxiters = 1000  # 最大迭代次数
    theta = pd.Series(np.zeros(n))  # 设置权重参数的初始值
    # cost_val = cosst_function(theta, X, y)
    # cost_record.append(cost_val)
    iters = 0
    while True:
        if iters >= maxiters:
            break
        grad = update_grad(theta, X, y)
        # 权重参数更新
        new_theta = update_theta(grad, theta, alpha)
        theta = new_theta
        # cost_update = cosst_function(new_theta, X, y)
        # cost_val = cost_update
        # cost_record.append(cost_val)
        iters += 1
    end = time.time()
    print("cost time: %f s" % (end - start))
    return theta, iters