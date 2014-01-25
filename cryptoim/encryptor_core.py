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

def encrypt(plaintext, key):
    """
        plaintext = string
        key = string (256 bits)
    """

    messages = __split_message(plaintext)
    roundkeys = __roundkey_separator(__key_expansion(key))
    return encrypt_round(messages, roundkeys)


def encrypt_round(messages, roundkeys):
    """
        encrypt_round
    """
    ciphertext = ''
    for msg in messages:
        msg = __add_roundkey(msg, roundkeys[14])
        for i in range(14):
            msg = __sub_bytes(msg)
            msg = __shift_rows(msg)
            msg = __mix_columns(msg)
            msg = __add_roundkey(msg, roundkeys[i])
        msg = __sub_bytes(msg)
        msg = __shift_rows(msg)
        msg = __add_roundkey(msg, roundkeys[15])
        ciphertext += __message_fusion(msg)
    return ciphertext



def __split_message(plaintext):
    """
        Splits message into 128 bits (16 characters) chunks and each of these
        chunks is then transformed into matrix with decimal value. These matrices
        are stored into list, creating a list of matrices.
    """
    message_chunks = []
    message_chunk = ''
    for i in range(len(plaintext)):
        message_chunk += plaintext[i]
        if len(message_chunk) == 16:
            message_chunks.append(message_chunk)
            message_chunk = ''
        if i == (len(plaintext)-1) and len(message_chunk) < 16:
            message_chunk += (16-len(message_chunk)) * '\x00'
            message_chunks.append(message_chunk)
            message_chunk = ''
    messages = []
    for chunk in message_chunks:
        matrix = [[], [], [], []]

        for i in range(4):
            for j in range(4):
                # Cool way to iterate and transform at the same time
                number = ord(chunk[4*i+j])
                matrix[i].append(number)

        messages.append(matrix)
    return messages

def __sub_bytes(message):
    """
        subbytes
    """
    for i in range(4):
        for j in range(4):
            hexadecimal = __convert_char_hex(message[i][j])
            message[i][j] = const.SBOX[int(hexadecimal[0], 16)][int(hexadecimal[1], 16)]
    return message

def __shift_rows(message):
    """
        Rotates 2nd, 3rd and 4th row of matrix, each by different amount.
        This rotation is done by using list slicing.
    """
    for i in range(4):
        message[i] = message[i][i:] + message[i][:i]
    return message

# 'state_mat' is the main State matrix, 'temp_mat' is a temp matrix of the same dimensions as 'state_mat'.
def __mix_columns(state_mat):
    """
        mix_columns
    """
    import copy

    g_mul = __g_mul
    temp_mat = copy.deepcopy(const.EMPTY_MAT_4_4)

    for column in range(4):
        temp_mat[0][column] = (g_mul(state_mat[0][column], 0x02) ^ g_mul(state_mat[1][column], 0x03) ^ state_mat[2][column] ^ state_mat[3][column])
        temp_mat[1][column] = (state_mat[0][column] ^ g_mul(state_mat[1][column], 0x02) ^ g_mul(state_mat[2][column], 0x03) ^ state_mat[3][column])
        temp_mat[2][column] = (state_mat[0][column] ^ state_mat[1][column] ^ g_mul(state_mat[2][column], 0x02) ^ g_mul(state_mat[3][column], 0x03))
        temp_mat[3][column] = (g_mul(state_mat[0][column], 0x03) ^ state_mat[1][column] ^ state_mat[2][column] ^ g_mul(state_mat[3][column], 0x02))

    state_mat = temp_mat # temp_mat.CopyTo(s, 0);
    return state_mat

def __g_mul(a, b):
    """
        g_mul, Bitwise multiplication
    """
    if b == 2:
        a = __convert_char_hex(a)
        result = const.GALOIS_TWO[int(a[0], 16)][int(a[1], 16)]
        return result
    if b == 3:
        a = __convert_char_hex(a)
        result = const.GALOIS_THREE[int(a[0], 16)][int(a[1], 16)]
        return result


def __message_fusion(message):
    """
        message_fusion
    """
    result_string = ''
    for i in range(4):
        for j in range(4):
            hexadecimal = __convert_char_hex(message[i][j])
            result_string += hexadecimal
    return result_string
