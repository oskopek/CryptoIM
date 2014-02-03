#!/usr/bin/env python
# encoding: utf-8

"""
   Copyright 2013-2014 CryptoIM Development Team

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import cryptoim.const as const
from cryptoim.common import __roundkey_separator, __key_expansion, __add_roundkey, __convert_char_hex

def decrypt(ciphertext, key):
    """
        Input: ciphertext - String
               key - String

        Output: plaintext - String

        Main decrypt method. This method prepares input values for the
        decryption and calls in the decryption method (decrypt_round).
        First it calls __ciphertext_fission method, which "cuts" the ciphertext to
        chunks with desired length (128 bits) puts them into matrices (4x4), each element
        of this matrix is 8 bits (1 byte). Afterwards calls in the __roundkey_separator
        method from the cryptoim.common module. This method creates matrix (4x4) of roundkeys,
        each of desired length (128 bits).
    """

    ciphertexts = __ciphertext_fission(ciphertext)
    extendedkey = __key_expansion(key)
    roundkeys = __roundkey_separator(extendedkey)
    return decrypt_round(ciphertexts, roundkeys)

def decrypt_round(ciphertexts, roundkeys):
    """
        Input: ciphertexts - List of lists of lists (List of 4x4 matrices)
               roundkeys - List of lists (4x4 Matrix)

        Output: plaintext - String

        Decryption method is using provided lists of roundkeys and ciphertext "chunks".
        Decryption does the same as encryption only in reversed steps. See encryptor_core
        documentation for more info.

        After algorithm proceeeds through the steps, it concatenates decrypted message
        chunks to the final plaintext using __message_completion method.
    """

    plaintext = ''
    for ctext in ciphertexts:
        ctext = __add_roundkey(ctext, roundkeys[15])
        ctext = __rshift_rows(ctext)
        ctext = __rsub_bytes(ctext)
        for i in range(13, -1, -1):
            ctext = __add_roundkey(ctext, roundkeys[i])
            ctext = __rmix_columns(ctext)
            ctext = __rshift_rows(ctext)
            ctext = __rsub_bytes(ctext)
        ctext = __add_roundkey(ctext, roundkeys[14])
        ctext = __message_completion(ctext)
        plaintext += ctext
        plaintext = plaintext.replace('\x00', '')
    return plaintext

def __mat_search(mat, elem):
    """
        Input: mat - List of lists (Desired matrix)
               elem - Element of matrix

        Output: tuple(row, column)

        This method is used to search in 2D arrays, matrices.
        Goes across the lines and looks for element, if it finds
        it, returns value of row and column, else passes to next line.
    """

    for i in range(len(mat)):
        try:
            mat[i].index(elem)
            return i, mat[i].index(elem)
        except ValueError:
            pass

def __rsub_bytes(ciphertext):
    """
        Input: ciphertext - List of lists (4x4 Matrix)

        Output: ciphertext - List of lists (4x4 Matrix)

        Reversed SubBytes step of the algorithm. For every byte (element of 4x4 Mat), it creates
        hexadecimal equivalent, which is then substitued according to look up table (SBOX)
        which can be found in cryptoim.const.
    """

    chex = __convert_char_hex

    for i in range(4):
        for j in range(4):
            idx = __mat_search(const.SBOX, ciphertext[i][j])
            ciphertext[i][j] = int((chex(idx[0])[1:] + chex(idx[1])[1:]), 16)
    return ciphertext

def __rshift_rows(ciphertext):
    """
        Input: ciphertext - List of lists (4x4 Matrix)

        Output: ciphertext - List of lists (4x4 Matrix)

        Reversed ShiftRows step of the algorithm. This step rotates elements in rows each by different
        amount depending on the row. First row stays the same, second is rotated to the right
        by one, third is rotated to the right by two, and fourth is rotated to the right by three.
    """

    for i in range(4):
        ciphertext[i] = ciphertext[i][-i:] + ciphertext[i][:-i]
    return ciphertext

def __rmix_columns(state_mat):
    """
        Input: state_mat - List of lists (4x4 Matrix)

        Output temp_mat - List of lists (4x4 Matrix)

        Reversed MixColumns step of the algorithm. Every column is multiplied by fixed matrix. Using the
        vector math and galois multiplication, it creates irreversible linear transformation. Basically each
        column is multiplied by some number and added back.
        More about this process:
        http://en.wikipedia.org/wiki/Rijndael_mix_columns
    """

    import copy

    g_mul = __g_mul
    temp_mat = copy.deepcopy(const.EMPTY_MAT_4_4)

    for column in range(4):
        temp_mat[0][column] = (g_mul(state_mat[0][column], 0x0E) ^ g_mul(state_mat[1][column], 0x0B) ^
                            g_mul(state_mat[2][column], 0x0D) ^ g_mul(state_mat[3][column], 0x09))
        temp_mat[1][column] = (g_mul(state_mat[0][column], 0x09) ^ g_mul(state_mat[1][column], 0x0E) ^
                            g_mul(state_mat[2][column], 0x0B) ^ g_mul(state_mat[3][column], 0x0D))
        temp_mat[2][column] = (g_mul(state_mat[0][column], 0x0D) ^ g_mul(state_mat[1][column], 0x09) ^
                            g_mul(state_mat[2][column], 0x0E) ^ g_mul(state_mat[3][column], 0x0B))
        temp_mat[3][column] = (g_mul(state_mat[0][column], 0x0B) ^ g_mul(state_mat[1][column], 0x0D) ^
                            g_mul(state_mat[2][column], 0x09) ^ g_mul(state_mat[3][column], 0x0E))

    state_mat = temp_mat # temp_mat.CopyTo(s, 0);
    return state_mat

def __g_mul(a, b):
    """
        Input: a - Integer
               b - Integer

        Output: result - Integer

        Galois multiplication or bitwise multiplication. This method is used in Reversed MixColumns
        step. Because of lack of better solution, we decided to use look up tables for results in this
        one. Tables can be found on wiki:
        http://en.wikipedia.org/wiki/Rijndael_mix_columns

        We put them into cryptoim.const, it returns result of multiplication according to tables.

        NOTE: "It looks the same, but isn't..." Purpose of this method is same as the one at encryptor
        but they differ in numbers.
    """

    if b == 9:
        a = __convert_char_hex(a)
        result = const.GALOIS_NINE[int(a[0], 16)][int(a[1], 16)]
        return result
    if b == 11:
        a = __convert_char_hex(a)
        result = const.GALOIS_ELEVEN[int(a[0], 16)][int(a[1], 16)]
        return result
    if b == 13:
        a = __convert_char_hex(a)
        result = const.GALOIS_THIRTEEN[int(a[0], 16)][int(a[1], 16)]
        return result
    if b == 14:
        a = __convert_char_hex(a)
        result = const.GALOIS_FOURTEEN[int(a[0], 16)][int(a[1], 16)]
        return result

def __ciphertext_fission(ciphertext):
    """
        Input: ciphertext - String

        Output: ciphertexts - List of lists of lists (List of 4x4 Matrices)

        Splits ciphertext into 128 bits (16 characters) chunks and each of these
        chunks is then transformed into matrix with decimal values. These matrices
        are stored into list, creating a list of matrices.
    """

    assert len(ciphertext) % 2 == 0
    ciphertexts = []
    hexadecimal = ''

    for _ in range((int(len(ciphertext)/32) )):
        matrix = [[], [], [], []]
        for i in range(32):
            hexadecimal += ciphertext[i]
            if len(hexadecimal) == 2:
                matrix[int(i/8)].append(int(hexadecimal, 16))
                hexadecimal = ''
        ciphertexts.append(matrix)
        ciphertext = ciphertext[32:]
    return ciphertexts

def __message_completion(ctext):
    """
        Input: ctext - List of lists (4x4 matrix)

        Output: result_string - String (Obviously)

        This method fuses the matrix back to string. Takes each byte (1 element of matrix)
        and converts it to letter, which it concatenates to the result string.
    """

    result_string = ''
    for i in range(4):
        for j in range(4):
            letter = chr(ctext[i][j])
            result_string += letter
    return result_string
