# aes-implementation

Educational implementation of **AES-128** organized as an MVC project, including:

- Random **128-bit key** generation
- Key expansion for round key generation
- Byte substitution with the **S-Box** and inverse S-Box
- Row shifting and inverse row shifting
- Column mixing and inverse column mixing
- Round key addition with XOR
- Text-to-block conversion, block encryption, and block decryption
- File-based workflow through an interactive CLI

> This repo is primarily for learning/training.

This project continues the arithmetic explored in the `abstract-algebra` repo and applies it to the full structure of AES-128.

## How to Run

Place the text you want to encrypt in `files/plaintext.txt`, then run:

```bash
python main.py
```

The interactive menu offers three operations:

| Option | Description | Reads from | Writes to |
|--------|-------------|------------|-----------|
| 1 | Generate Key | — | `files/key.txt` |
| 2 | Encrypt Text | `files/plaintext.txt`, `files/key.txt` | `files/encrypted.txt` |
| 3 | Decrypt Text | `files/encrypted.txt`, `files/key.txt` | `files/decrypted.txt` |

> The `files/` directory is created automatically on first run. Keep `key.txt` safe — it is required to decrypt a ciphertext.

## Files

- `main.py`  
  Entry point; starts the interactive CLI.

- `src/view/ui.py`  
  Presents the menu and dispatches user choices to the controller.

- `src/controller/control.py`  
  Orchestrates the workflow:
  - Creates and manages the `files/` directory
  - Reads plaintext, key, and ciphertext from files
  - Calls model functions and writes results back to files

- `src/model/cipher.py`  
  AES core logic:
  - Applies the four round operations to each 4x4 block
  - Runs 10 encryption or decryption rounds
  - Generates a random 128-bit key with `os.urandom`

- `src/model/abstract_algebra.py`  
  Finite field and matrix operations used by AES:
  - Multiplication in **GF(2^8)**
  - Polynomial division over **GF(2)**
  - Extended Euclidean Algorithm for multiplicative inverse
  - Matrix/vector helpers used in S-Box and MixColumns

- `src/model/aes_modules/s_box.py`  
  Implements the AES substitution layer:
  - Computes the multiplicative inverse in **GF(2^8)**
  - Applies the affine transformation defined by the AES spec
  - Provides both `sbox` and `inv_sbox`

- `src/model/aes_modules/shift_rows.py`  
  Implements `shift_rows` and `inv_shift_rows`.

- `src/model/aes_modules/mix_columns.py`  
  Implements `mix_columns` and `inv_mix_columns` using matrix multiplication in **GF(2^8)**.

- `src/model/aes_modules/add_round_key.py`  
  Implements the XOR between the current AES state and the round key.

- `src/model/aes_modules/key_expansion.py`  
  Implements the AES-128 key schedule:
  - Builds the initial words from the input key
  - Applies the `g` function with rotation, S-Box substitution, and `rcon`
  - Expands a single key into the 11 round keys needed by AES-128

- `src/utils/text_converter.py`  
  Handles all data conversion:
  - UTF-8 encoding/decoding
  - PKCS-style padding to a multiple of 16 bytes
  - Conversion between flat byte lists and 4x4 AES state matrices (column-major order)
  - Conversion of byte blocks to binary or hexadecimal strings
  - Parsing of hex key strings and hex ciphertexts back into usable arrays

## Brief Explanation

- AES works on **16-byte blocks**, represented here as **4x4 matrices** of bytes.
- Each block is transformed over multiple rounds using four main operations: **SubBytes**, **ShiftRows**, **MixColumns**, and **AddRoundKey**.
- The **S-Box** is not a hardcoded lookup table here; its output is computed from the multiplicative inverse in **GF(2^8)** followed by an affine transformation.
- **MixColumns** and the S-Box both rely on **GF(2^8)** arithmetic, which is why the algebra module is central to the implementation.
- The key schedule expands one 128-bit key into 11 round keys (one initial, nine intermediate, one final).
- The project includes all inverse operations so encrypted blocks can be fully decrypted back to the original plaintext.
- Text is encoded as UTF-8, padded to fit AES blocks, encrypted block by block, and stored as a hex string. Decryption reverses every step.
