# Missing Reindeer (300)

## Problem

> Not only elves took control of Santa's Christmas factory but they kidnapped Rudolf as well. Our cyber spies managed to capture an email related to Santa's favorite reindeer. Can you help them decrypt the message?

* [crypto_missing_reindeer.zip](./crypto_missing_reindeer.zip)

## Solution

1. We are given an email with two attachments: an RSA public key (`pubkey.der`) and a message encrypted using that key (`secret.enc`). Copy the contents of these two files into their own respective files with the proper names.

2. Let's look at the decoded contents of the public key file so we can see the public modulus and exponent. We can do this by running `openssl rsa -pubin -in pubkey.der -text -noout`. which shows:

    ```
    RSA Public-Key: (2048 bit)
    Modulus:
        00:e6:23:97:28:84:b1:f4:d7:22:bd:d5:ee:5b:eb:
        84:cb:84:76:0c:2e:d0:ff:af:d9:3c:d6:03:0f:b2:
        0d:79:30:90:3b:d1:73:1d:c7:4c:95:4a:23:07:53:
        03:df:d7:1b:88:5c:d6:6e:98:5b:f7:59:ed:17:a9:
        85:f7:e7:d8:37:c8:57:bd:31:a1:47:d7:4d:a2:61:
        49:28:58:fa:5f:cf:b8:92:30:87:8e:f4:ff:fc:ff:
        92:fc:29:29:89:32:64:54:af:b5:1b:b7:ab:25:3f:
        ef:d5:b3:57:bf:83:a6:39:f1:53:20:4a:fc:56:28:
        f3:e0:20:22:c6:94:9d:c2:3c:b1:9d:2f:d6:39:b6:
        d5:98:7a:c3:32:a0:1d:d2:3b:43:7a:67:77:bb:96:
        7f:80:e5:22:e9:41:e5:f9:72:16:0a:ed:55:6d:b7:
        39:39:19:80:64:22:ae:1a:7d:c9:b1:99:96:fd:b7:
        b2:91:41:47:2d:68:03:df:f4:2a:71:3d:b5:7a:c0:
        78:fc:a4:8d:1a:68:61:42:3d:e3:a1:2e:d9:cf:af:
        b8:31:e5:d6:9b:92:d7:19:63:d0:23:22:8c:26:12:
        ea:33:4a:65:2c:46:12:1f:50:5d:1b:5a:55:12:24:
        c6:9f:c8:23:9c:fe:10:93:de:68:09:5f:71:53:15:
        96:67
    Exponent: 3 (0x3)
    ```

3. As you can see, the public exponent is small, which means that we can break this RSA encryption using a small public exponent attack. There is no padding (aka this is textbook RSA) and the message is small, so this attack works. You can learn more about the attack on [BitsDeep](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-2/).

4. We write a script that loads the encrypted data, converts it to an integer, takes the 3rd (since that's the value of `e`) root of that integer, and finally converts the result to ASCII. The script is inspired by [Dvd848's solution to the Safe RSA 2018 PicoCTF challenge](https://github.com/Dvd848/CTFs/blob/master/2018_picoCTF/Safe%20RSA.md#solution). The decrypted output is `We are in Antarctica, near the independence mountains.\nHTB{w34k_3xp0n3n7_ffc896}`, which contains the flag.

5. [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool) can solve this challenge. So, just extract the email attachments, Base64 decode the secret like so `cat secret.enc | base64 -d > secret_decoded.enc`, and then run RsaCtfTool: `python3 RsaCtfTool.py --publickey pubkey.der --uncipherfile secret_decoded.enc`, which will print the decrypted message after a few minutes.

### Flag

`HTB{w34k_3xp0n3n7_ffc896}`
