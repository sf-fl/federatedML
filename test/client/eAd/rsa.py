# -*- coding: utf-8 -*-

# 求两个数字的最大公约数（欧几里得算法）
import gmpy2
import random


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

'''
扩展欧几里的算法
计算 ax + by = 1中的x与y的整数解（a与b互质）
'''
def ext_gcd(a, b):
    if b == 0:
        x1 = 1
        y1 = 0
        x = x1
        y = y1
        r = a
        return r, x, y
    else:
        r, x1, y1 = ext_gcd(b, a % b)
        x = y1
        y = x1 - a // b * y1
        return r, x, y


'''
超大整数超大次幂然后对超大的整数取模
(base ^ exponent) mod n
'''
import time


def exp_mode(base, exponent, n):
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []

    pre_base = base
    base_array.append(pre_base)

    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n
        base_array.append(next_base)
        pre_base = next_base

    a_w_b = __multi(base_array, bin_array, n)
    return a_w_b % n


def __multi(array, bin_array, n):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
        result = result % n  # 加快连乘的速度
    return result


# 生成公钥私钥，p、q为两个超大质数
def gen_key(p, q):
    n = p * q
    fy = (p - 1) * (q - 1)  # 计算与n互质的整数个数 欧拉函数
    e = 65537  # 选取e   一般选取65537
    # generate d
    a = e
    b = fy
    r, x, y = ext_gcd(a, b)
    # 计算出的x不能是负数，如果是负数，说明p、q、e选取失败，不过可以把x加上fy，使x为正数，才能计算。
    if x < 0:
        x = x + fy
    d = x
    # 返回：   公钥     私钥
    return (n, e), (n, d)


# 加密 m是被加密的信息 加密成为c
def encrypt(m, pubkey):
    n = pubkey[0]
    e = pubkey[1]

    c = exp_mode(m, e, n)
    return c


# 解密 c是密文，解密为明文m
def decrypt(c, selfkey):
    n = selfkey[0]
    d = selfkey[1]

    m = exp_mode(c, d, n)
    return m

def get_prime(rs):
    p = int(gmpy2.mpz_urandomb(rs,4096))
    if p % 2 != 1:
        p = p + 1
    while not gmpy2.is_prime(p):
        p = p + 2
    return p

if __name__ == "__main__":
    '''公钥私钥中用到的两个大质数p,q，都是1024位'''
    time_st = time.time()
    rs = gmpy2.random_state(1)
    p = int(get_prime(rs))
    q = int(get_prime(rs))
    print(p)
    print(q)
    '''生成公钥私钥'''
    pubkey, selfkey = gen_key(p, q)
    '''需要被加密的信息转化成数字，长度小于秘钥n的长度，如果信息长度大于n的长度，那么分段进行加密，分段解密即可。'''
    m = 123
    print("待加密信息-->%s" % m)
    '''信息加密，m被加密的信息，c是加密后的信息'''
    c = encrypt(m, pubkey)
    print("被加密后的密文-->%s" % c)
    '''信息解密'''
    d = decrypt(c, selfkey)
    print("被解密后的明文-->%s" % d)
    print(time.time()-time_st)