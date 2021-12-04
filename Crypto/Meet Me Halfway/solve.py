import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from tqdm import tqdm
from itertools import permutations

padding = b"cyb3rXm45!@#"
alphabet = b"0123456789abcdef"
encrypted_flag = binascii.unhexlify(
    "7564c7bdd466450e70bc68cc5f7832762144d187e188d70f84884fb0fb5ab8f8e3332e24e847d8bebbd146df941a8f8197280738faa788261509fe9495b37db15424cdf3682f2743e08437d2f229a7b8f40f44b1aea07c74999692fa70365f75"
)

custom_known_text = pad(bytes.fromhex("13371337"), 16)
custom_ciphertext = binascii.unhexlify("85c88e874465c9c3db46caeaca525690")

encrypt_table = {}
for key in tqdm(permutations(alphabet, 4), desc="Bruteforcing 1st Key"):
    key = padding + bytes(key)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_custom = cipher.encrypt(custom_known_text)
    encrypt_table[encrypted_custom] = key

decrypt_table = {}
for key in tqdm(permutations(alphabet, 4), desc="Bruteforcing 2nd Key"):
    key = bytes(key) + padding
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_custom = cipher.decrypt(custom_ciphertext)
    decrypt_table[decrypted_custom] = key

print("Finding Key Intersection...")
encrypt_table_set = set(encrypt_table.keys())
decrypt_table_set = set(decrypt_table.keys())
for encrypt_decrypt_value in encrypt_table_set.intersection(decrypt_table_set):
    encrypt_key = encrypt_table[encrypt_decrypt_value]
    decrypt_key = decrypt_table[encrypt_decrypt_value]
    break
print("1st Key Found: %s" % encrypt_key)
print("2nd Key Found: %s" % decrypt_key)

cipher1 = AES.new(encrypt_key, AES.MODE_ECB)
cipher2 = AES.new(decrypt_key, AES.MODE_ECB)
flag_intermediate = cipher2.decrypt(encrypted_flag)
flag = cipher1.decrypt(flag_intermediate).decode()
print("Flag: %s" % flag)
