import numpy as np
import src.model.abstract_algebra as aa


def table_positions(b):
    # It's relevant to see those 4 bits to locate on the default table given by AES to verify answers
    left_4_bits = (b >> 4) & 0b1111
    right_4_bits = b & 0b1111
    print(f"Left 4 bits: {bin(left_4_bits)} or {hex(left_4_bits)}")
    print(f"Right 4 bits: {bin(right_4_bits)} or {hex(right_4_bits)}")
    print("")


def sbox(b):
    irr = 0b100011011
    yf = aa.multiplicative_inverse(irr, b)

    # Beginning the S-box programming

    mat_a = np.array([
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1]
    ], dtype=int)

    c = np.array([1, 1, 0, 0, 0, 1, 1, 0], dtype=int)

    vet_b = aa.byte_to_array(bin(yf)[2::].zfill(8)[::-1])

    byte_res = aa.affine_transform(mat_a, vet_b, c)

    sub_byte = aa.arr_to_byte(byte_res)

    return sub_byte


def inv_sbox(b):
    irr = 0b100011011

    # Using the inverse of a matrix to decrypt later
    mat_a_inv = np.array([
        [0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0]
    ], dtype=int)

    c = np.array([1, 0, 1, 0, 0, 0, 0, 0], dtype=int)

    vet_b = aa.byte_to_array(bin(b)[2::].zfill(8)[::-1])

    byte_res = aa.affine_transform(mat_a_inv, vet_b, c)

    inv_byte = aa.arr_to_byte(byte_res)

    yf = aa.multiplicative_inverse(irr, inv_byte) # The multiplicative inverse needs to be moved as the last step

    return yf