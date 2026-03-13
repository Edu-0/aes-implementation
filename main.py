import src.model.cipher as cipher
import src.utils.text_converter as tc

if __name__ == "__main__":
    key = cipher.generate_key()
    key_array = tc.string_to_array(key)

    text = "Super text for testings"
    byte_blocks = tc.start_encoding_conversion(text)
    rk_list = cipher.expand_key(key_array)

    final_encrypted = cipher.encrypt(byte_blocks, rk_list)
    print(f"Encrypted block -> ")
    cipher.print_hex(final_encrypted)

    print(f"Encrypted hex code: {tc.byte_blocks_to_hex_string(final_encrypted)}\n")

    decrypted_block = cipher.decrypt(final_encrypted, rk_list)
    print(f"Decrypted block -> ")
    cipher.print_hex(decrypted_block)

    print(f"Decrypted hex code: {tc.byte_blocks_to_hex_string(decrypted_block)}")
    decrypted_text = tc.start_decoding_conversion(decrypted_block)
    print(f"Decrypted text: {decrypted_text}\n")