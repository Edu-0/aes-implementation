import os
from pathlib import Path
import src.model.cipher as cipher
import src.utils.text_converter as tc
from src.model.cipher import sum_nonce


def get_files_dir():
    src_dir = Path("ui.py").resolve().parents[0]
    files_dir = f"{src_dir}\\files"

    if not os.path.exists(files_dir):
        os.makedirs(files_dir)

    return files_dir


def generate_key(files_dir):
    key_path = os.path.join(files_dir, "key.txt")
    with open(key_path, "w") as file:
        file.write(cipher.generate_key())
    print("Key generated on a file, store it on a safe place for it to be used again.")


def generate_nonce(files_dir):
    nonce_path = os.path.join(files_dir, "nonce.txt")
    with open(nonce_path, "w") as file:
        file.write(cipher.generate_key()) # Reutilizing the same key generation technique, as it's almost the same
    print("Nonce generated on a file, store it on a safe place for reutilize.")

def encrypt_plaintext(files_dir):
    try:
        plaintext_path = os.path.join(files_dir, "plaintext.txt")
        with open(plaintext_path, "r", encoding='utf-8') as file:
            plaintext = file.read()
            if len(plaintext) < 1:
                print("Invalid plaintext for encryption")
    except FileNotFoundError:
        print("\"plaintext.txt\" file not found in \"files\" directory")
        return

    try:
        key_path = os.path.join(files_dir, "key.txt")
        with open(key_path, "r") as file:
            initial_key = file.readline()
            if len(initial_key) < 32:
                print("Invalid key read from files, it must have a size of 32 chars in hex")
    except FileNotFoundError:
        print(f"Key file not found, add a key.txt file in \"files\" folder")
        return

    try:
        nonce_path = os.path.join(files_dir, "nonce.txt")
        with open(nonce_path, "r") as file:
            initial_nonce = file.readline()
            if len(initial_nonce) < 32:
                print("Invalid Nonce read from files, it must have a size of 32 chars in hex")
    except FileNotFoundError:
        print(f"Nonce file not found, add a nonce.txt file in \"files\" folder")
        return

    key_array = tc.key_string_to_array(initial_key)
    nonce_array = tc.key_string_to_array(initial_nonce)

    byte_blocks = tc.start_encoding_conversion(plaintext)
    rk_list = cipher.expand_key(key_array)

    final_encrypted = cipher.encrypt_decrypt(byte_blocks, rk_list, nonce_array)

    encrypted_path = os.path.join(files_dir, "encrypted.txt")
    with open(encrypted_path, "w") as file:
        file.write(tc.byte_blocks_to_hex_string(final_encrypted))
    print("Text encrypted and saved on files folder")


def decrypt_text(files_dir):
    try:
        encrypted_path = os.path.join(files_dir, "encrypted.txt")
        with open(encrypted_path, "r", encoding='utf-8') as file:
            encrypted = file.read()
            if len(encrypted) < 1:
                print("Invalid encrypted for decryption")
    except FileNotFoundError:
        print("\"encrypted.txt\" file not found in \"files\" directory")
        return

    try:
        key_path = os.path.join(files_dir, "key.txt")
        with open(key_path, "r") as file:
            initial_key = file.readline()
            if len(initial_key) < 32:
                print("Invalid key read from files, it must have a size of 32 chars in hex")
    except FileNotFoundError:
        print(f"Key file not found, add a key.txt file in \"files\" folder")
        return

    try:
        nonce_path = os.path.join(files_dir, "nonce.txt")
        with open(nonce_path, "r") as file:
            initial_nonce = file.readline()
            if len(initial_nonce) < 32:
                print("Invalid Nonce read from files, it must have a size of 32 chars in hex")
    except FileNotFoundError:
        print(f"Nonce file not found, add a nonce.txt file in \"files\" folder")
        return

    key_array = tc.key_string_to_array(initial_key)
    nonce_array = tc.key_string_to_array(initial_nonce)

    byte_list = tc.hex_string_to_byte_list(encrypted)
    encrypted_text_array = tc.array_creator(byte_list)

    rk_list = cipher.expand_key(key_array)
    decrypted_block = cipher.encrypt_decrypt(encrypted_text_array, rk_list, nonce_array)

    decrypted_path = os.path.join(files_dir, "decrypted.txt")
    with open(decrypted_path, "w", encoding='utf-8') as file:
        try:
            file.write(tc.start_decoding_conversion(decrypted_block))
        except UnicodeDecodeError:
            print("Error: Wrong decrypting key or corrupted text.")
            return
    print("Text decrypted and saved on files folder")