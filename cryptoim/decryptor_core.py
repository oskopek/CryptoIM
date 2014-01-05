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
        decrypt
    """
    ciphertexts = __ciphertext_fission(ciphertext)
    extendedkey = __key_expansion(key)
    roundkeys = __roundkey_separator(extendedkey)
    return decrypt_round(ciphertexts, roundkeys)

def decrypt_round(ciphertexts, roundkeys):
    """
        decrypt_round
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

def __ciphertext_fission(ciphertext):
    """
        Ciphertext splitter, splits ciphertext, and puts chunks into matrices
        which are then put into list.
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

def __mat_search(mat, elem):
    """
        Mat Search, returns tuple (row, column)
    """
    for i in range(len(mat)):
        try:
            mat[i].index(elem)
            return i, mat[i].index(elem)
        except ValueError:
            pass

def __rsub_bytes(ciphertext):
    """
        Reversed SubBytes step
    """
    chex = __convert_char_hex

    for i in range(4):
        for j in range(4):
            idx = __mat_search(const.SBOX, ciphertext[i][j])
            ciphertext[i][j] = int((chex(idx[0])[1:] + chex(idx[1])[1:]), 16)
    return ciphertext

def __rshift_rows(ciphertext):
    """
        Reversed shift rows
    """
    for i in range(4):
        ciphertext[i] = ciphertext[i][-i:] + ciphertext[i][:-i]
    return ciphertext

def __rmix_columns(state_mat):
    """
        Reversed mix_columns
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
        g_mul, Bitwise multiplication
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

def __message_completion(ctext):
    """
        message_completion
    """
    result_string = ''
    for i in range(4):
        for j in range(4):
            letter = chr(ctext[i][j])
            result_string += letter
    return result_string
