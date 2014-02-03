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
        Input: plaintext - String
               key - String

        Output: ciphertext - String

        Main encrypt method. This method prepares input values for the
        actual encryption and calls in the encryption method (encrypt_round).
        First it calls __split_message method, which "cuts" the message to
        chunks with desired length (128 bits) puts them into matrices (4x4), each element
        of this matrix is 8 bits (1 byte), and then calls in the
        __roundkey_separator method from the cryptoim.common module. This method creates
        matrix (4x4) of roundkeys, each of desired length (128 bits).
    """

    messages = __split_message(plaintext)
    roundkeys = __roundkey_separator(__key_expansion(key))
    return encrypt_round(messages, roundkeys)


def encrypt_round(messages, roundkeys):
    """
        Input: messages - List of lists of lists (List of 4x4 matrices)
               roundkeys - List of lists (4x4 Matrix)

        Output: ciphertext - String

        Encryption method is using provided lists of roundkeys and message "chunks".
        Encryption algorithm used is Advanced Encryption Standard. It consists of
        four steps, which repeat demanded number of times (in our case we used 14
        repetitions, plus initial and final round). Method uses following methods(steps):
        cryptoim.common.__add_roundkey, __sub_bytes, __shift_rows, __mix_columns.

        You can find more information here:
        http://en.wikipedia.org/wiki/Advanced_Encryption_Standard

        NOTE: This algorithm doesnt use standard __split_message.

        After algorithm proceeeds throught the steps, it concatenates encrypted message
        chunks to the final ciphertext using __message_fusion method.
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

def __sub_bytes(message):
    """
        Input: message - List of lists (4x4 Matrix)

        Output: message - List of lists (4x4 Matrix)

        SubBytes step of the algorithm. For every byte (element of 4x4 Mat), it creates
        hexadecimal equivalent, which is then substitued according to look up table (SBOX)
        which can be found in cryptoim.const.
    """

    for i in range(4):
        for j in range(4):
            hexadecimal = __convert_char_hex(message[i][j])
            message[i][j] = const.SBOX[int(hexadecimal[0], 16)][int(hexadecimal[1], 16)]
    return message

def __shift_rows(message):
    """
        Input: message - List of lists (4x4 Matrix)

        Output: message - List of lists (4x4 Matrix)

        ShiftRows step of the algorithm. This step rotates elements in rows each by different
        amount depending on the row. First row stays the same, second is rotated to the left by one
        third is rotated to the left by two, and fourth is rotated to the left by three.
    """
    for i in range(4):
        message[i] = message[i][i:] + message[i][:i]
    return message

def __mix_columns(state_mat):
    """
        Input: state_mat - List of lists (4x4 Matrix)

        Output temp_mat - List of lists (4x4 Matrix)

        MixColumns step of the algorithm. Every column is multiplied by fixed matrix. Using the vector math
        and galois multiplication, it creates irreversible linear transformation. Basically each column is
        multiplied by some number and added back.

        More about this process:
        http://en.wikipedia.org/wiki/Rijndael_mix_columns

        The 'state_mat' is the main state matrix, 'temp_mat' is a temp matrix of the same dimensions as 'state_mat'.
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
        Input: a - Integer
               b - Integer

        Output: result - Integer

        Galois multiplication or bitwise multiplication. This method is used in MixColumns step.
        Because of lack of better solution, we decided to use look up tables for results in this
        one.

        Tables can be found on wiki:
        http://en.wikipedia.org/wiki/Rijndael_mix_columns

        We put them into cryptoim.const, it returns result of multiplication according to tables.
    """

    if b == 2:
        a = __convert_char_hex(a)
        result = const.GALOIS_TWO[int(a[0], 16)][int(a[1], 16)]
        return result
    if b == 3:
        a = __convert_char_hex(a)
        result = const.GALOIS_THREE[int(a[0], 16)][int(a[1], 16)]
        return result

def __split_message(plaintext):
    """
        Input: plaintext - String

        Output: messages - List of lists of lists (List of 4x4 Matrices)

        Splits message into 128 bits (16 characters) chunks and each of these
        chunks is then transformed into matrix with decimal values. These matrices
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

def __message_fusion(message):
    """
        Input: messages - List of lists (4x4 matrix)

        Output: result_string - String (Obviously)

        This method fuses the matrix back to string. Takes each byte (1 element of matrix)
        and converts it to letter, which it concatenates to the result string.
    """

    result_string = ''
    for i in range(4):
        for j in range(4):
            hexadecimal = __convert_char_hex(message[i][j])
            result_string += hexadecimal
    return result_string
