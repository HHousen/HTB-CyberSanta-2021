# XMAS Spirit (300)

## Problem

> Now that elves have taken over Santa has lost so many letters from kids all over the world. However, there is one kid who managed to locate Santa and sent him a letter. It seems like the XMAS spirit is so strong within this kid. He was so smart that thought of encrypting the letter in case elves captured it. Unfortunately, Santa has no idea about cryptography. Can you help him read the letter?

* [crypto_xmas_spirit.zip](./crypto_xmas_spirit.zip)

## Solution

1. We are given a `challenge.py` file that encrypts a file called `letter.pdf` and stores it to `encrypted.bin`. We have `encrypted.bin` so it looks we like just need to write a function to decrypt this file by doing what `challenge.py` but in reverse.

2. The important encryption line is `enc = (a*byte + b) % mod`. The inverse of this is `dec = (byte * modinv(a, mod) - b) % mod`, which can be found using [modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic). I don't understand modular arithmetic that well so I'm not going to explain how I solved this. This solution also probably isn't the most efficient, but it does decrypt the file in a matter of seconds, so its fast enough.

3. We use a function to compute the modular multiplicative inverse using the extended Euclidean algorithm. More info on [this StackOverflow answer](https://stackoverflow.com/a/9758173).

4. Also, the encryption script uses a `mod` value of 256, determines `a` by selecting an a such that `1 <= a < mod` and `gcd(a, mod) == 1`, and `b` is a random integer such that `1 <= b < mod`. We can simply try every combination of these values since there are not that many combinations. However, since decrypting the file takes several seconds, we need a way to determine if a combination is the correct one without decrypting the whole file. This is possible because every PDF starts with the same bytes. These are known as [magic bytes](https://en.wikipedia.org/wiki/List_of_file_signatures). For PDFs, the bytes are `25 50 44 46 2D` in hex or `%PDF-` in ASCII. So, we will loop through every combination of `a` and `b` and decrypt the first 5 bytes of the `encrypted.bin` file. If they decrypt to `%PDF-`, then we will decrypt the rest of the file and save to to `letter.pdf`.

5. The flag is found in plain text in the decrypted `letter.pdf` file, which I've [included in this repo](./letter.pdf). Apparently, this is an affine cipher (according to the flag), so there is likely a more basic and straightforward solution than this.

### Flag

`HTB{4ff1n3_c1ph3r_15_51mpl3_m47h5}`
