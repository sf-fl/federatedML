import gmpy2
import random
import time
import binascii

def get_prime(rs):
    p = gmpy2.mpz_urandomb(rs, 1024)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p

def L(x, n):
    return (x - 1) // n

class Paillier:
    p = 5
    q = 7
    n = p*q
    lmd = (p-1)*(q-1)
    g = n + 1
    if gmpy2.gcd(L(gmpy2.powmod(g, lmd, n ** 2), n), n) != 1:
        print('[!] g is not good enough')
        exit()
    pk = [n, g]
    sk = [n,lmd]

    def __init__(self):
        rs = gmpy2.random_state(1)
        self.p = get_prime(rs)
        self.q = get_prime(rs)
        self.n = self.p * self.q
        self.lmd = (self.p - 1) * (self.q - 1)
        self.g = self.n + 1
        if gmpy2.gcd(L(gmpy2.powmod(self.g, self.lmd, self.n ** 2), self.n), self.n) != 1:
            print('[!] g is not good enough')
            exit()
        self.pk = [self.n, self.g]
        self.sk = [self.n, self.lmd]

    def get_public_key(self):
        return self.pk

    def get_private_key(self):
        return self.pk

    def encipher(self, plaintext, *pub_key):
        if pub_key is None:
            pub_key = self.pk
        if (isinstance(plaintext, int)):
            m = plaintext
        else:
            m = int(binascii.hexlify(plaintext.encode('utf-8')), 16)
        print(m)
        n, g = pub_key
        r = random.randint(1, n ** 2)
        ciphertext = gmpy2.powmod(g, m, n ** 2) * gmpy2.powmod(r, n, n ** 2) % (n ** 2)
        return ciphertext

    def decipher(self, ciphertext, pk, sk):
        [n, g] = pk
        lmd = sk
        u = gmpy2.invert(L(gmpy2.powmod(g, lmd, n ** 2), n), n) % n
        m = L(gmpy2.powmod(ciphertext, lmd, n ** 2), n) * u % n
        print(m)
        plaintext = m
        return plaintext

    def plus(self, c1, c2, pk):
        n, g = pk
        c12 = (c1 * c2) % (n ** 2)
        return c12

    def multiply(self, c, cons, pk):
        n, g = pk
        if cons > 1:
            ct = c
            for i in range(1, cons):
                ct = (ct * c) % (n ** 2)
            return ct
        else:
            return c


