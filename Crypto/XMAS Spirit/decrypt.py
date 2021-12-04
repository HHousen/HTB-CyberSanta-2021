#!/usr/bin/python3

from math import gcd
from tqdm import tqdm

# `egcd` and `modinv` code from https://stackoverflow.com/a/9758173
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m


a_values = [a for a in range(256) if gcd(a, 256) == 1]
mod = 256
b_values = range(1, mod)


def decrypt_bytes(dt, a, b):
    res = b""
    for byte in dt:
        dec = (byte * modinv(a, mod) - b) % mod
        res += bytes([dec])
    return res


def decrypt(dt):
    for a in tqdm(a_values, "Bruteforcing a and b"):
        for b in b_values:
            res = decrypt_bytes(dt[:5], a, b)
            if res.startswith(b"%PDF-"):
                res = decrypt_bytes(tqdm(dt, desc="Decrypting File"), a, b)
                return res


dt = open("encrypted.bin", "rb").read()

res = decrypt(dt)

f = open("letter.pdf", "wb")
f.write(res)
f.close()
