import os
from pathlib import Path
import src.model.cipher as cipher
import src.utils.text_converter as tc

def get_files_dir():
    src_dir = Path("ui.py").resolve().parents[2]
    files_dir = f"{src_dir}\\files"

    if not os.path.exists(files_dir):
        os.makedirs(files_dir)

    return files_dir


def generate_key(files_dir):
    key_path = os.path.join(files_dir, "key.txt")
    with open(key_path, "w") as file:
        file.write(cipher.generate_key())
    print("Key generated on a file, store it on a safe place for it to be used again.")


def encrypt_plaintext(files_dir):
    try:
        plaintext_path = os.path.join(files_dir, "plaintext.txt")
        with open(plaintext_path, "r", encoding='utf-8') as file:
            plaintext = file.read()
            if len(plaintext) < 1:
                print("Invalid plaintext for encryption")
    except FileNotFoundError:
        print("\"plaintext.txt\" file not found in \"files\" directory")
    print(plaintext)
    try:
        key_path = os.path.join(files_dir, "key.txt")
        with open(key_path, "r") as file:
            initial_key = file.readline()
            if len(initial_key) < 32:
                print("Invalid key read from files, it must have a size of 32 chars in hex")
    except FileNotFoundError:
        print(f"Key file not found, add a key.txt file in \"files\" folder")

    print(initial_key)

    key_array = tc.string_to_array(initial_key)

    byte_blocks = tc.start_encoding_conversion(plaintext)
    rk_list = cipher.expand_key(key_array)

    final_encrypted = cipher.encrypt(byte_blocks, rk_list)
    tc.byte_blocks_to_hex_string(final_encrypted)

    encrypted_path = os.path.join(files_dir, "encrypted.txt")
    with open(encrypted_path, "w") as file:
        file.write(tc.byte_blocks_to_hex_string(final_encrypted))
    print("Text encrypted and saved on files folder")