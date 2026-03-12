import numpy as np
import src.aes.s_box as sb
import src.aes.shift_rows as sr
import src.aes.mix_columns as mc
import src.aes.add_round_key as ark
import src.utils.text_converter as tc
import src.aes.key_expansion as ke


def print_hex_simple(bb):
    for i in range(bb.shape[0]):
        for j in range(bb.shape[1]):
            print(f"{bb[i, j]:02X}", end=" ")
        print()


def print_hex(blocks):
    for k, bb in enumerate(blocks):
        print(f"Block {k}")
        for i in range(bb.shape[0]):
            for j in range(bb.shape[1]):
                print(f"{bb[i, j]:02X}", end=" ")
            print()
        print()


# Working with the entire byte block with S-Box, byte by byte
def s_box_block(bb):
    res_array = np.zeros((4, 4), dtype=int)
    for i in range(res_array.shape[0]):
        for j in range(res_array.shape[1]):
            res_array[i][j] = sb.sbox(bb[i][j])

    return res_array


def inv_s_box_block(bb):
    res_array = np.zeros((4, 4), dtype=int)
    for i in range(res_array.shape[0]):
        for j in range(res_array.shape[1]):
            res_array[i][j] = sb.inv_sbox(bb[i][j])

    return res_array


def generate_keys(ik):
    return ke.words_to_keys(ke.key_expansion(ik))


def encrypt_block(state, round_keys):
    # Starting round
    state = ark.add_round_key(state, round_keys[0])

    # Rounds 1 to 9
    for i in range(1, 10):
        state = s_box_block(state)
        state = sr.shift_rows(state)
        state = mc.mix_columns(state)
        state = ark.add_round_key(state, round_keys[i])

    # Final round, no MixColumns
    state = s_box_block(state)
    state = sr.shift_rows(state)
    state = ark.add_round_key(state, round_keys[10])
    return state


def decrypt_block(state, round_keys):
    # Starting round
    state = ark.add_round_key(state, round_keys[-1])

    # Rounds 9 to 1
    for i in range(9, 0, -1):
        state = sr.inv_shift_rows(state)
        state = inv_s_box_block(state)
        state = ark.add_round_key(state, round_keys[i])
        state = mc.inv_mix_columns(state)

    # Final round, no MixColumns
    state = sr.inv_shift_rows(state)
    state = inv_s_box_block(state)
    state = ark.add_round_key(state, round_keys[0])
    return state


# Encrypt and Decrypt will start the process
def encrypt(bbs, rks):
    encrypted_blocks = []
    for i in range(len(bbs)): # Passing block by block from the byte block list
        encrypted_blocks.append(encrypt_block(bbs[i], rks))
    return encrypted_blocks


def decrypt(bbs, rks):
    decrypted_blocks = []
    for i in range(len(bbs)):
        decrypted_blocks.append(decrypt_block(bbs[i], rks))
    return decrypted_blocks


if __name__ == "__main__":
    # Test key used for the early examples
    initial_key = np.array(
        [
            [0xAC, 0x19, 0x28, 0x57],
            [0x77, 0xFA, 0xD1, 0x5C],
            [0x66, 0xDC, 0x29, 0x00],
            [0xF3, 0x21, 0x41, 0x6A]
        ],
        dtype=int
    )

    # key = tc.array_creator(list(os.urandom(16))) Key generation

    text = "Super text for testings"
    byte_blocks = tc.start_encoding_conversion(text)
    rk_list = generate_keys(initial_key)

    final_encrypted = encrypt(byte_blocks, rk_list)
    print(f"Encrypted block -> ")
    print_hex(final_encrypted)

    print(f"Encrypted hex code: {tc.byte_blocks_to_hex_string(final_encrypted)}\n")

    decrypted_block = decrypt(final_encrypted, rk_list)
    print(f"Decrypted block -> ")
    print_hex(decrypted_block)

    print(f"Decrypted hex code: {tc.byte_blocks_to_hex_string(decrypted_block)}")
    decrypted_text = tc.start_decoding_conversion(decrypted_block)
    print(f"Decrypted text: {decrypted_text}\n")