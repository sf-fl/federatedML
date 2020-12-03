import math
import time
import numpy as np
import pandas as pd
import rsa
import rsa.core
from client.eAd import paillier
from client.proxy import client_proxy

lamb = 1
scal = 100

def cal_ub(theta,x,y):
    temp1 = np.dot(theta.T, x)
    temp2 = 2 * y.iloc[0]
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


def generate_random(n):
    return np.random.random_integers((scal**3),(scal**3)*10,size=n)  # todo


def update_grad(theta_b,x_b,y_b):
    # 生成 key_b 和 ubb 并发出
    theta = theta_b.apply(lambda x: int(x*scal))
    ppk_b, psk_b = paillier.gen_key()
    ub_list = []
    time_start = time.time()
    for i in range(x_b.shape[0]):
        xb = x_b.iloc[i].apply(lambda x: int(x*scal))
        yb = y_b.iloc[i].apply(lambda x: int(x*scal))
        ub = cal_ub(theta,xb,yb)
        ub_code = int(paillier.encipher(ub,ppk_b))
        if i % 100 == 0:
            print('%.f%%' % (i/x_b.shape[0]*100))
        # ub_code = int2bytes(ub_code, rsa_len//8-11)
        # ub_code = str(rsa.encrypt(ub_code, rpk_b))
        ub_list.append(ub_code)
    print('100%')
    print('ubb计算耗时：',time.time()-time_start)
    gradA_pb, ua_list, ppk_a = client_proxy.learn_1(ub_list,ppk_b)

    # 计算gbra
    time_start = time.time()
    gradB_pa = theta.apply(lambda x: int(paillier.encipher(lamb * 2 * (scal ** 3) * x, ppk_a)))
    for i in range(x_b.shape[0]):
        xb = x_b.iloc[i].apply(lambda x: int(x*scal))
        yb = y_b.iloc[i].apply(lambda x: int(x*scal*scal))
        ub = cal_ub(theta, xb, yb)

        ua = ua_list[i]
        u_pa = paillier.plus(ua, ub, ppk_a)
        u_pa_i = [paillier.multiply(u_pa, x, ppk_a) for x in xb]
        for num, ux in enumerate(u_pa_i):
            gradB_pa[num] = paillier.plus(ux, gradB_pa[num], ppk_a)
        if i % 100 == 0:
            print('%.f%%' % (i / x_b.shape[0] * 100))
    rb = generate_random(x_b.shape[1])
    rb_pb = [int(paillier.encipher(int(r), ppk_a)) for r in rb]
    for num, r in enumerate(rb_pb):
        gradB_pa[num] = paillier.plus(r, gradB_pa[num], ppk_a)
    gradB_pa = list(gradB_pa)
    print('gbra计算耗时：',time.time()-time_start)

    # 给A解密
    time_start = time.time()
    gradA_r = []
    for grad in gradA_pb:
        gradA_r.append(paillier.decipher(grad,ppk_b,psk_b))
    print('Gar解密耗时：',time.time()-time_start)

    gradB_r = client_proxy.learn_2(gradB_pa,gradA_r)

    gradB = gradB_r - rb

    return gradB / 4 * pow(10, -9)


def update_theta(grad, theta, alpha):
    theta = theta - alpha * grad
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


if __name__ == '__main__':
    a = 100
    rsa_len = 4096
    time_start = time.time()
    # 生成 key_b 和 ub 并发出
    ppk_b, psk_b = paillier.gen_key()
    rpk_b, rsk_b = rsa.newkeys(rsa_len)
    print(rpk_b.n)
    print(rpk_b.e)
    print(rsk_b.d)
    ar = rsa.core.encrypt_int(a,rpk_b.e,rpk_b.n)
    ar3 = pow(ar,100,rpk_b.n)
    ar_r = rsa.core.decrypt_int(ar3,rsk_b.d,rsk_b.n)

    ap = int(paillier.encipher(a,ppk_b))
    apr = rsa.core.encrypt_int(ap,rpk_b.e,rpk_b.n)
    aprm = pow(apr,100,rpk_b.n)
    aprm_r = rsa.core.decrypt_int(aprm,rsk_b.d,rsk_b.n) % (psk_b[0] ** 2)
    aprm_rp = paillier.decipher(aprm_r,ppk_b,psk_b)
    cost_time = time.time()-time_start
    print(cost_time)