# Warehouse Maintenance (325)

## Problem

> Elves are out of control! They have compromised the database of Santa's warehouse. We have revealed the endpoint and we need to find a way to execute commands in the database. Unfortunately, every command needs to be signed by an Elf named Frost. Can you find a way in?

* [crypto_warehouse_maintenance.zip](./crypto_warehouse_maintenance.zip)

## Solution

1. Looking at the `challenge.py` source code we notice that if option 2 is selected, we can send a script that will be executed using the `util.executeScript` function if we provide the correct signature:

    ```python
    elif option=='2':
        print('Please send your script and its signature.\n> ')
        resp = input().strip()
        resp = json.loads(resp)
        if check_signature(resp['script'], resp['signature']):
            script = bytes.fromhex(resp['script'])
            res = executeScript(script)

            print(res+'\n')
        else:
            print('Are you sure mister Frost signed this?\n')
    ```

2. In `util.py`, we see that `executeScript` connects to a MySQL database and will run any SQL queries in our input.

3. So, the challenge is going to be to forge a signature. Signatures are created and checked using the `` and `` functions respectively:

    ```python
    def create_sample_signature():
        dt = open('sample','rb').read()
        h = hashlib.sha512( salt + dt ).hexdigest()

        return dt.hex(), h

    def check_signature(dt, h):
        dt = bytes.fromhex(dt)
        
        if hashlib.sha512( salt + dt ).hexdigest() == h:
            return True
    ```

4. We can get a sample signature, which provides us with a script, `55534520786d61735f77617265686f7573653b0a234d616b65207375726520746f2064656c6574652053616e74612066726f6d2075736572732e204e6f7720456c7665732061726520696e206368617267652e`, and a signature, `68708f48015143f048cb1d5916d1c1feee086709ee5a0af55cd9039005ebba517a4c10f5c59e3ede4a0aa3a375d7640a3ea31f840997683b3412e8d903d24c21`. The information, provided with the details about how a signature is created (`hashlib.sha512( salt + dt ).hexdigest()`) suggest that this is a "hash length extension" attack. To recap, we know the the plaintext of some of the data (`dt`) being hashed, the hash of the `salt + dt`, and the length range of the `salt` (8 to 100 bytes). By the way, the text that the server is hashing is the same text in the `sample` file included in the challenge zip.

5. You can learn more about hash length extension attacks in this wonderful article: [Everything you need to know about hash length extension attacks](https://blog.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks). This article discusses this program [iagox86/hash_extender](https://github.com/iagox86/hash_extender), which can be used to solve this challenge. Essentially, the TL;DR of this attack is that "given a hash that is composed of a string with an unknown prefix, an attacker can append to the string and produce a new hash that still has the unknown prefix."

6. However, we will be using [bwall/HashPump](https://github.com/bwall/HashPump) because it has Python bindings and will make it easier for us to bruteforce guess the length of the salt.

7. We run the [solution script](hash_length_extension_attack.py) once with `data_to_add` set to `\nshow tables;` to see what tables exist in the database. This shows that there are two tables: materials and users. So, we run the script again with `data_to_add` set to `\nSELECT * FROM materials;` to see what is in the materials table. The flag is then printed to the screen.

8. Output of [solution script](hash_length_extension_attack.py):

    ```
    [+] Opening connection to 138.68.136.191 on port 30463: Done
    [*] Retrieved signature/hexdigest: 68708f48015143f048cb1d5916d1c1feee086709ee5a0af55cd9039005ebba517a4c10f5c59e3ede4a0aa3a375d7640a3ea31f840997683b3412e8d903d24c21
    [*] Original data: USE xmas_warehouse;
        #Make sure to delete Santa from users. Now Elves are in charge.
    [*] Adding '
        SELECT * FROM materials;' to hash
    Bruteforcing key length:   0%|                                                                                                 | 0/92 [00:00<?, ?it/s]
    Bruteforcing key length:  16%|██████████████▎                                                                         | 15/92 [00:05<00:26,  2.94it/s]
    [+] Key Length: 23
    [+] Flag: HTB{b'h45hpump_15_50_c001_h0h0h0'}
    Bruteforcing key length:  16%|██████████████▎                                                                         | 15/92 [00:06<00:33,  2.28it/s]
    [*] Closed connection to 138.68.136.191 port 30463
    ```

### Flag

`HTB{h45hpump_15_50_c001_h0h0h0}`
