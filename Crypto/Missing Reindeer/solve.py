# Code inspired by https://github.com/Dvd848/CTFs/blob/master/2018_picoCTF/Safe%20RSA.md#solution.

import gmpy2
import binascii
from base64 import b64decode

e = 3
with open("secret.enc") as secret:
    secret_bytes = b64decode(secret.read())
cipher_str = int.from_bytes(secret_bytes, "big")

gc = gmpy2.mpz(cipher_str)  # Using gmpy2.mpz for full precision
ge = gmpy2.mpz(e)

root, exact = gmpy2.iroot(gc, ge)  # Take the 3rd root of the cipher text
print(binascii.unhexlify(hex(root)[2:]).decode())  # Decode to ASCII
