import numpy as np
import src.s_box as sb
import src.abstract_algebra as aa

rcon = [
    0x00,   # Round 1
    0x01,
    0x02,
    0x04,
    0x08,
    0x10,
    0x20,
    0x40,
    0x80,
    0x1B,
    0x36    # Round 11
]


# Takes the columns and transform into the initial key, the first 4 words
def initial_key_generator(a):
    initial_key = []
    for i in range(a.shape[0]):
        word = []
        for j in range(a.shape[1]):
            word.append(int(a[j][i]))
        initial_key.append(word)
    return initial_key


def g(word, r):
    word = np.roll(word, -1) # Shift left the values
    word = [int(sb.aes_sbox(word[i])) for i in range(len(word))] # Apply S-Box
    word[0] ^= rcon[r] # XOR with the specified table (A table is better than generating the numbers, as it's O(1) here)
    return word


# Main Algorithm
def key_expansion(init_array):
    w = list(initial_key_generator(init_array)) # It must have a len(w) of 44 by the end

    for i in range(4, 44):
        temp = w[i-1] # Value used for XOR with the next byte
        if i % 4 == 0: # If it's the last of 4 words, it'll be used on the g function
            temp = g(temp, i//4)
        w.append(aa.xor_vector(w[i-4], temp))
    w = [np.array(x) for x in w] # Converting to work with NumPy as it's better optimized
    return w