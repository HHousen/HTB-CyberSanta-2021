# Meet Me Halfway (325)

## Problem

> Evil elves have deployed their own cryptographic service. The keys are unknown to everyone but them. Fortunately, their encryption algorithm is vulnerable. Could you help Santa break the encryption and read their secret message?

* [crypto_meet_me_halfway.zip](./crypto_meet_me_halfway.zip)

## Solution

1. Connect to get the encrypted flag: `nc 167.99.89.198 31352` to get `7564c7bdd466450e70bc68cc5f7832762144d187e188d70f84884fb0fb5ab8f8e3332e24e847d8bebbd146df941a8f8197280738faa788261509fe9495b37db15424cdf3682f2743e08437d2f229a7b8f40f44b1aea07c74999692fa70365f75`. For this challenge we will need a set of plaintext and ciphertext strings so I encrypt `13371337` (by sending `{"pt": "13371337"}`) and get `85c88e874465c9c3db46caeaca525690` back as the encrypted data. We need to send our input as JSON because the `challenge.py` file expects it in that format.

2. This challenge is nearly identical to the "Double DES" challenge from PicoCTF 2021, and I've already [written a guide to solve that challenge](https://github.com/HHousen/PicoCTF-2021/tree/6f9f20933e1ed467dbdfcdd7af027a06439e2d84/Cryptography/Double%20DES#double-des). The difference is that this challenge uses AES instead of DES and it uses some slightly different data types.

3. So, my [solution script](./solve.py) is very similar to [my solution script for PicoCTF "Double DES"](https://github.com/HHousen/PicoCTF-2021/blob/6f9f20933e1ed467dbdfcdd7af027a06439e2d84/Cryptography/Double%20DES/script.py). Make sure you have `pycryptodome` and `tqdm` installed the run the script. You can install them via `pip3 install pycryptodome tqdm`.

4. Double AES is vulnerable to a [meet-in-the-middle attack](https://en.wikipedia.org/wiki/Meet-in-the-middle_attack). [This StackExchange answer](https://security.stackexchange.com/a/122626) explains the attack for Double DES (which for all purpose is the same as AES). Basically, you start with the plain text, and then you bruteforce every possible key, encrypt the plain text, and store the results in a dictionary. Then, you take the original encrypted data (`85c88e874465c9c3db46caeaca525690` in this case) and bruteforce decrypt it using every possible key, storing the results as you go. Then, you find the intersection between the encrypted and decrypted values. The keys corresponding to the overlapping value are the two keys used in the Double DES algorithm.

5. 16 bytes of padding are used in `challenge.py`, but 12 of those bytes are known and are stored in the `const` variable, so we only need to bruteforce 4 bytes for the 1st key and 4 bytes for the second. Importantly, the first key is `key + const` and the second is `const + key`.

6. Running the [solution script](./solve.py) finds the keys and the flag:

    ```
    Bruteforcing 1st Key: 43680it [00:00, 91201.63it/s]
    Bruteforcing 2nd Key: 43680it [00:00, 92324.93it/s]
    Finding Key Intersection...
    1st Key Found: b'cyb3rXm45!@#b180'
    2nd Key Found: b'37c2cyb3rXm45!@#'
    Flag: https://www.youtube.com/watch?v=DZMv9XO4Nlk
    HTB{m337_m3_1n_7h3_m1ddl3_0f_3ncryp710n}
    ```

### Flag

`HTB{m337_m3_1n_7h3_m1ddl3_0f_3ncryp710n}`
