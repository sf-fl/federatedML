#!/usr/bin/env python
import gmpy2
import random
import time
import libnum
def get_prime(rs):
    p = gmpy2.mpz_urandomb(rs, 1024)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p
def L(x, n):
    return (x - 1) // n
def keygen():
    rs = gmpy2.random_state(1)
    p = get_prime(rs)
    q = get_prime(rs)
    n = p * q
    lmd = (p - 1) * (q - 1)
    #g = random.randint(1, n ** 2)
    g = n + 1
    if gmpy2.gcd(L(gmpy2.powmod(g, lmd, n ** 2), n), n) != 1:
        print('[!] g is not good enough')
        exit()
    pk = [n, g]
    sk = lmd
    return pk, sk
def encipher(plaintext, pk):
    if(plaintext.isdigit()):
        m=int(plaintext)
    else:
        m = libnum.s2n(plaintext)
    n, g = pk
    r = random.randint(1, n ** 2)
    c = gmpy2.powmod(g, m, n ** 2) * gmpy2.powmod(r, n, n ** 2) % (n ** 2)
    return c
def plus(c1,c2,pk):
    n,g=pk
    c12=(c1*c2)%(n**2)
    return c12
def multiply(c,t,pk):
    n,g=pk
    if t>1:
        ct=c
        for i in range(1,t):
            ct=(ct*c)%(n**2)
        return ct
    else:
        return c
def decipher(c, pk, sk):
    [n, g] = pk
    lmd = sk
    u = gmpy2.invert(L(gmpy2.powmod(g, lmd, n ** 2), n), n) % n
    plaintext = L(gmpy2.powmod(c, lmd, n ** 2), n) * u % n
    return plaintext
if __name__ == '__main__':
    pk, sk = keygen()
    print('pk:', pk)
    print('sk:', sk)
    plaintext1 = input('Please input your message: ')
    plaintext2 = input('Please input your message: ')
    print(time.time())
    for i in range(10000):
        ciphertext1 = encipher(plaintext1,pk)
        ciphertext2 = encipher(plaintext2,pk)
        plus1=plus(ciphertext1,ciphertext2,pk)
        plaintext = decipher(plus1, pk, sk)
        if i%1000==0:
            print('palintext:',plaintext)
    print(time.time())


