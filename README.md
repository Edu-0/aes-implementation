# aes-implementation

Small, educational scripts implementing the main parts of **AES-128** for study purposes, including:

- Key expansion for round key generation
- Byte substitution with the **S-Box** and inverse S-Box
- Row shifting and inverse row shifting
- Column mixing and inverse column mixing
- Round key addition with XOR
- Text-to-block conversion, block encryption, and block decryption

> This repo is primarily for learning/training and includes a print-based example flow in `main.py`.

This project continues the arithmetic explored in the `abstract-algebra` repo and applies it to the structure of AES.

## Files

- `main.py`  
	Demonstrates the full AES flow for a sample text:
	- Converts UTF-8 text into 4x4 byte blocks
	- Generates round keys from an initial 16-byte key
	- Encrypts each block using the AES round structure
	- Decrypts the result back into text
	- Prints intermediate outputs in hexadecimal form

- `src/aes/abstract_algebra.py`  
	Contains the finite field and matrix operations used by AES:
	- Multiplication in **GF(2^8)**
	- Polynomial multiplication/division over **GF(2)**
	- Extended Euclidean Algorithm for multiplicative inverse
	- Matrix/vector helpers used in S-Box and MixColumns operations

- `src/aes/s_box.py`  
	Implements the AES substitution layer:
	- Computes the multiplicative inverse in **GF(2^8)**
	- Applies the affine transformation used by the AES S-Box
	- Provides both `sbox` and `inv_sbox`

- `src/aes/shift_rows.py`  
	Implements:
	- `shift_rows`
	- `inv_shift_rows`

- `src/aes/mix_columns.py`  
	Implements:
	- `mix_columns`
	- `inv_mix_columns`
	using AES matrix multiplication in **GF(2^8)**

- `src/aes/add_round_key.py`  
	Implements the XOR between the current AES state and the round key.

- `src/aes/key_expansion.py`  
	Implements the AES-128 key schedule:
	- Builds the initial words from the input key
	- Applies the `g` function with rotation, S-Box substitution, and `rcon`
	- Expands the key into the round keys used during encryption/decryption

- `src/utils/text_converter.py`  
	Handles text and block conversion:
	- UTF-8 encoding/decoding
	- Padding to a multiple of 16 bytes
	- Conversion between byte lists and 4x4 AES state matrices
	- Conversion of encrypted/decrypted blocks to binary or hexadecimal strings

## Brief Explanation

- AES works on **16-byte blocks**, represented here as **4x4 matrices** of bytes.
- For AES, the state is transformed over multiple rounds using four main operations: **SubBytes**, **ShiftRows**, **MixColumns**, and **AddRoundKey**.
- The **S-Box** is not treated as a hardcoded lookup-only concept here; its logic is constructed from finite field arithmetic and an affine transformation.
- **MixColumns** and parts of the S-Box depend on arithmetic in **GF(2^8)**, which is why the supporting algebra code is part of the implementation.
- The key schedule expands one initial **128-bit key** into all round keys needed by AES-128.
- The project also includes the inverse operations so encrypted blocks can be decrypted back into the original plaintext.
- Text input is encoded as UTF-8, padded to fit AES blocks, encrypted block by block, and then decoded again after decryption.
