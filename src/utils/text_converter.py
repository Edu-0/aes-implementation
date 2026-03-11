import numpy as np


# Simple conversion to binary
def encode_text(text):
    return list(text.encode("UTF-8"))


def decode_text(byte_text):
    bits_fix = int(byte_text, 2).to_bytes(len(byte_text) // 8, "big")
    padding = bits_fix[-1] # Gets the last bit as it will always have padding
    bits_fix = bits_fix[:-padding] # Removing the padding as it can conflict with the UTF-8 reading to decode
    return bits_fix.decode("UTF-8")


# This function makes sure that the list has a size multiple of 16 for it to be able to divide into blocks of 4x4
def normalize_list(bin_list):
    len_bin_list = len(bin_list)
    missing = 16 - len_bin_list % 16
    if missing == 0:
        missing = 16
    for i in range(missing):
        bin_list.append(missing)
    return bin_list


def array_creator(bin_list):
    array_list = []
    for i in range(0, len(bin_list), 16):
        array_list.append(np.array(np.reshape(bin_list[i:i+16], (4, 4), order="F"), dtype=int)) # AES uses the column-major order, from Fortran, so I specify here in order = "F"
    return array_list


def byte_blocks_to_text(byte_blocks):
    decoded_string = ""
    for _, bb in enumerate(byte_blocks):
        for byte in bb.flatten(order="F"):
            decoded_string += f"{byte:08b}"
    return decoded_string


def start_encoding_conversion(text):
    return array_creator(normalize_list(encode_text(text)))


def start_decoding_conversion(byte_blocks):
    return byte_blocks_to_text(byte_blocks)