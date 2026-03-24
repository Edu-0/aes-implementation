import os
import numpy as np
import src.model.aes_modules.s_box as sb
import src.model.aes_modules.shift_rows as sr
import src.model.aes_modules.mix_columns as mc
import src.model.aes_modules.add_round_key as ark
import src.model.aes_modules.key_expansion as ke
from src.model.abstract_algebra import xor_matrix


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


def expand_key(ik):
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


# The decryption and encryption specific algorithms were done on past commits when it was done in EBC, now it's CTR mode
def encrypt_decrypt(bbs, rks, n_arr):
    encrypted_blocks = []
    for i in range(len(bbs)): # Passing block by block from the byte block list
        encrypted_blocks.append(xor_matrix(encrypt_block(n_arr, rks), bbs[i]))
        n_arr = sum_nonce(n_arr)
    return encrypted_blocks


# Returns the usable key for the program and the key string
def generate_key():
    key = os.urandom(16)
    return key.hex().upper()


def sum_nonce(n_arr):
    for i in range(n_arr.shape[0]-1, -1, -1):
        for j in range(n_arr.shape[1]-1, -1, -1):
            if n_arr[i][j] == 255:
                continue
            else:
                n_arr[i][j] += 1
                return n_arr
    return n_arr