import numpy as np


def gf_mul(f, g):
    result = 0
    for i in range(len(bin(g)[2:])):
        if (g >> i) & 1:
            temp = f
            for _ in range(i):
                of = bin((temp & 0x80) >> 7)[2:]
                temp = (temp << 1) & 0xFF
                if of == "1":
                    temp ^= 0b11011

            result ^= temp
    return result


def gf2_mul(f, g):
    result = 0
    for i in range(len(bin(g)[2:])):
        if (g >> i) & 1:
            temp = f
            for _ in range(i):
                temp = temp << 1
            result ^= temp
    return result


def deg(b):
    for i in range(len(bin(b)[2:]) - 1, -1, -1):
        if (b >> i) & 1:
            return i
    return 0


def gf2_div(a, b):
    q = 0
    r = a

    while deg(r) >= deg(b):
        shift = deg(r) - deg(b)
        q |= (1 << shift)
        r ^= (b << shift)
        if r == 0:
            break
    return q, r


def gf_egcd(a, b):
    if b == 0:
        return a, 1, 0

    q, r = gf2_div(a, b)
    g, x1, y1 = gf_egcd(b, r)

    x = y1
    y = x1 ^ gf_mul(q, y1)

    return g, x, y


def multiplicative_inverse(a, b):
    return gf_egcd(a, b)[2]


# Working with matrices in GF(2)
def byte_to_array(byte):
    return np.array(list(byte), dtype=int)


def vet_sum(mat_a, c):
    byte_res = np.zeros(mat_a.shape[0], dtype=int)
    for i in range(mat_a.shape[0]):
        byte_res[i] = mat_a[i] ^ c[i]
    return byte_res


def mat_vet_mul(mat_a, vet_b):
    vet_res = np.zeros(mat_a.shape[0], dtype=int)
    for i in range(mat_a.shape[0]):
        for j in range(vet_b.shape[0]):
            vet_res[i] ^= mat_a[i][j] & vet_b[j]
    return vet_res


def mat_mul(mat_a, mat_b):
    vet_res = np.zeros((mat_a.shape[0], mat_b.shape[1]), dtype=int)
    for i in range(mat_a.shape[0]):
        for j in range(mat_b.shape[1]):
            for k in range(mat_a.shape[1]):
                vet_res[i][j] ^= gf_mul(mat_a[i][k], mat_b[k][j])
    return vet_res


# Affine Transform is the main operation on S-Box, which finds the values equals to the ones on the table
def affine_transform(mat_a, vet_b, c):
    return vet_sum(mat_vet_mul(mat_a, vet_b), c)


def arr_to_byte(arr):
    sub_byte = 0
    for i in range(arr.shape[0]):
        sub_byte |= arr[i] << i
    return sub_byte


def xor_matrix(mat_a, mat_b):
    vet_res = np.zeros((mat_a.shape[0], mat_b.shape[1]), dtype=int)
    for i in range(mat_a.shape[0]):
        for j in range(mat_b.shape[1]):
            vet_res[i][j] = mat_a[i][j] ^ mat_b[i][j]
    return vet_res