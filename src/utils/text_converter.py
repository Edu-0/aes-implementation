import numpy as np


# Simple conversion to binary
def encode_text(text):
    return list(text.encode("UTF-8"))


def decode_text(byte_text):
    bits_fix = int(byte_text, 2).to_bytes(len(byte_text) // 8, "big")
    return bits_fix.decode("UTF-8")


def array_creator(byte_list, block_size=16):
    blocks = []
    full_len = (len(byte_list) // block_size) * block_size
    for i in range(0, full_len, 16):
        block = np.array(byte_list[i:i + 16]).reshape((4, 4), order="F")
        blocks.append(block)
    rest = byte_list[full_len:] # 0 to 15 bytes
    return blocks, rest


def byte_blocks_to_bin_string(byte_blocks):
    decoded_string = ""
    for _, bb in enumerate(byte_blocks):
        for byte in bb.flatten(order="F"):
            decoded_string += f"{byte:08b}"
    return decoded_string


def byte_blocks_to_hex_string(byte_blocks):
    decoded_string = ""
    for _, bb in enumerate(byte_blocks):
        for byte in bb.flatten(order="F"):
            decoded_string += f"{byte:02X}"
    return decoded_string


def vector_to_hex_string(vec):
    return ''.join(f"{b:02X}" for b in vec)


def start_encoding_conversion(text):
    return array_creator(encode_text(text))


def start_decoding_conversion(byte_blocks):
    return decode_text(byte_blocks_to_bin_string(byte_blocks))


def key_string_to_array(ks):
    cut_string = [ks[i:i + 2] for i in range(0, len(ks), 2)]
    hex_list = [int(cs, 16) for cs in cut_string]

    hex_array = np.array(np.reshape(hex_list, (4, 4)), dtype=int)

    return hex_array

def hex_string_to_byte_list(hex_string):
    cut_string = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    return [int(cs, 16) for cs in cut_string]