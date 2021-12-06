# pip3 install pwntools hashpumpy tqdm
import hashpumpy
from pwn import *
from tqdm import tqdm
import json
import re

host = args.HOST or "138.68.136.191"
port = int(args.PORT or 30463)
io = connect(host, port)

io.recvuntil(b">")
io.sendline(b"1")
given_script_signature = json.loads(io.recvuntil(b"\n").strip())
hexdigest = given_script_signature["signature"]
log.info("Retrieved signature/hexdigest: %s", hexdigest)

with open("sample", "r") as sample_dt:
    original_data = sample_dt.read()
log.info("Original data: %s", original_data)
data_to_add = "\nSELECT * FROM materials;"  # Used `\nshow tables;` initially
log.info("Adding '%s' to hash", data_to_add)

# Loop through all possible lengths of the key and perform a hash length extension
# attack until we guess the length correctly and the message "Are you sure mister
# Frost signed this?" is not shown.
for key_length in tqdm(range(8, 100), "Bruteforcing key length"):
    io.recvuntil(b">")
    io.sendline(b"2")

    new_hexdigest, new_message = hashpumpy.hashpump(
        hexdigest, original_data, data_to_add, key_length
    )

    payload = f'{{"script": "{new_message.hex()}", "signature": "{new_hexdigest}"}}'
    io.sendline(bytes(payload, encoding="ascii"))
    data = io.recvuntil(b"Are you sure mister Frost signed this?", timeout=1)
    if not data.endswith(b"this?"):
        log.success("Key Length: %i", key_length)
        io.recvline()
        contains_flag = io.recvuntil(b"\n")
        flag_finding_regex = re.compile(b"HTB\{(.*)\}")
        flag = re.findall(flag_finding_regex, contains_flag)[0]
        log.success("Flag: HTB{%s}", flag)
        break
