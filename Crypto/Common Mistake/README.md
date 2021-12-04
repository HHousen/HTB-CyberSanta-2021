# Common Mistake (300)

## Problem

> Elves are trying very hard to communicate in perfect secrecy in order to keep Santa's warehouse. Unfortunately, their lack of knowledge about cryptography leads them to common mistakes.

* [crypto_common_mistake.zip](./crypto_common_mistake.zip)

## Solution

1. Looking at the challenge we see that the public modulus, n, is the same for both messages. Searching for a "RSA Common Modulus Attack" finds some writeups and code to solve problems like these. The code I used is explained in [RSA: Common Modulus attack with extended Euclidean algorithm](https://blog.0daylabs.com/2015/01/17/rsa-common-modulus-attack-extended-euclidean-algorithm/).

2. [The solution script](rsa_common_modulus_attack.py) is nearly identical to [a0xnirudh's RSA: Common modulus attack.py](https://github.com/a0xnirudh/Exploits-and-Scripts/blob/master/RSA%20Attacks/RSA:%20Common%20modulus%20attack.py). I formatted the code slightly better and added in a line (`print("Plain Text: ", binascii.unhexlify(hex(self.m)[2:]).decode())`) to convert the decrypted message to ASCII. Running the script will produce the flag.

### Flag

`HTB{c0mm0n_m0d_4774ck_15_4n07h3r_cl4ss1c}`
