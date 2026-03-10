import numpy as np
import src.s_box as sb
import src.shift_rows as sr
import src.mix_columns as mc
import src.add_round_key as ark
import src.text_converter as tc


def print_hex(blocks):
    for k, bb in enumerate(blocks):
        print(f"Block {k}")
        for i in range(bb.shape[0]):
            for j in range(bb.shape[1]):
                print(f"{bb[i, j]:02X}", end=" ")
            print()
        print()


def s_box_block(bb):
    res_array = np.zeros((4, 4), dtype=int)
    for i in range(res_array.shape[0]):
        for j in range(res_array.shape[1]):
            res_array[i][j] = sb.aes_sbox(bb[i][j])

    return res_array


def shift_rows(bb):
    return sr.shift_rows(s_box_block(bb))


def mix_columns(bb):
    return mc.mix_columns(sr.shift_rows(s_box_block(bb)))


def add_round_key(bb, round_key):
    return ark.add_round_key(mc.mix_columns(sr.shift_rows(s_box_block(bb))), round_key)


def start_cryptography(bb, rk):
    return add_round_key(bb, rk)


def cryptograph_blocks(bbs, rk):
    converted_blocks = []
    for i in range(len(bbs)):
        converted_blocks.append(start_cryptography(bbs[i], rk))
    return converted_blocks


test_key = np.array(
    [
        [0xAC, 0x19, 0x28, 0x57],
        [0x77, 0xFA, 0xD1, 0x5C],
        [0x66, 0xDC, 0x29, 0x00],
        [0xF3, 0x21, 0x41, 0x6A]
    ],
    dtype=int
)

text = "Super text for testings"
byte_blocks = tc.start_encoding_conversion(text)
encrypted_blocks = cryptograph_blocks(byte_blocks, test_key)

print_hex(encrypted_blocks)