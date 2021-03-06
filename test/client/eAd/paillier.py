import gmpy2
import random
import time
import binascii


def get_prime(rs):
    p = gmpy2.mpz_urandomb(rs,32)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p


def L(x, n):
    return (x - 1) // n


def gen_key():
    rs = gmpy2.random_state(1)
    p = int(get_prime(rs))
    q = int(get_prime(rs))
    n = p * q
    lmd = (p - 1) * (q - 1)
    g = n + 1
    if gmpy2.gcd(L(gmpy2.powmod(g, lmd, n ** 2), n), n) != 1:
        print('[!] g is not good enough')
        exit()
    pk = [n, g]
    sk = [n, lmd]
    return pk,sk


def encipher(plaintext, pub_key):
    if isinstance(plaintext, int):
        m = plaintext
    else:
        if isinstance(plaintext, float):
            m = int(plaintext)
        else:
            m = int(binascii.hexlify(plaintext.encode('utf-8')), 16)
    n, g = pub_key
    if m < 0:
        m += n
    # print(m)
    r = random.randint(1, n ** 2)
    ciphertext = gmpy2.powmod(g, m, n ** 2) * gmpy2.powmod(r, n, n ** 2) % (n ** 2)
    return ciphertext


def decipher(ciphertext, pk, sk):
    [n, g] = pk
    lmd = sk[1]
    u = gmpy2.invert(L(gmpy2.powmod(g, lmd, n ** 2), n), n) % n
    m = L(gmpy2.powmod(ciphertext, lmd, n ** 2), n) * u % n
    # print(m)
    plaintext = int(m)
    if plaintext > n/2:
        plaintext = plaintext - n
    # print(plaintext)
    return plaintext


def plus(c1, c2, pk):
    n, g = pk
    c12 = (c1 * c2) % (n ** 2)
    return int(c12)


def multiply(c, cons, pk): # todo int强转
    n, g = pk
    if not isinstance(cons, int):
        print("常数非整")
        cons = int(cons//1)
    if cons > 0:
        ct = c
        for i in range(1, cons):
            ct = (ct * c) % (n ** 2)
        return int(ct)
    else:
        return 1

