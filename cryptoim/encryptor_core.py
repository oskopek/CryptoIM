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

def encrypt(plaintext, key):
    """
        plaintext = string
        key = string (256 bytes)
    """

    messages = __split_message(plaintext)
    roundkeys = __roundkey_separator(__key_expansion(key))
    return encrypt_round(messages,roundkeys)


def encrypt_round(messages,roundkeys):
    """
        encrypt_round
    """
    ciphertext = ""
    for msg in messages:
        msg = __add_roundkey(msg,roundkeys[14])
        for i in range(14):
            print (msg)
            msg = __sub_bytes(msg)
            print (msg)
            msg = __shift_rows(msg)
            print (msg)
            msg = __mix_columns(msg)
            msg = __add_roundkey(msg,roundkeys[i])
        msg = __sub_bytes(msg)
        msg = __shift_rows(msg)
        msg = __add_roundkey(msg,roundkeys[15])
        ciphertext += msg
    return ciphertext
        

def __key_expansion(key):
    """
        key_expansion
    """
    import hashlib
    extendedkey = ''
    keyhash = key       # Assigns key value to the keyhash, for later use in cycle
    for i in range(32):
        keyhash = hashlib.sha224(keyhash.encode('utf-8')).hexdigest()
        extendedkey += keyhash
    extendedkey = extendedkey[:256]
    return extendedkey

def __roundkey_separator(extendedkey):
    """
        Returns list of 16 matrices, these are 128 bit roundkeys used for encryption,
        from there 16 matrices will be only 14 used. For opimization purpose was used
        index k instead of another cycle.
    """
    k = 0
    roundkeys = []
    for k in range(16):
        roundkey = [[], [], [], []] # Matrix (list of lists)
        for i in range(4):
            for j in range(4):
                # Converts letter to decimal number
                decimal = ord(extendedkey[k])
                # Appends 4 numbers into each row of matrix
                roundkey[i].append(decimal)
                k += 1
        roundkeys.append(roundkey)
    return roundkeys

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
            message_chunk += (16-len(message_chunk))*"\x00"
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
    # TODO: Check if this works as expected

def __add_roundkey(message, roundkey):
    """
        add_roundkey
    """
    # Uses one matrix of each as input
    for i in range(4):
        for j in range(4):
            message[i][j] = message[i][j]^roundkey[i][j] # XOR
    return message

def __sub_bytes(message):
    """
        subbytes
        TODO: The lines are too long according to pylint (sbox list definiton)
    """
    sbox = [[0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
            [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
            [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
            [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
            [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
            [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
            [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
            [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
            [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
            [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
            [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
            [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
            [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
            [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
            [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
            [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]]

    for i in range(4):
        for j in range(4):
            hexadecimal = hex(message[i][j]).lstrip("0x")
            if len(hexadecimal)<2:
                hexadecimal = "0"+hexadecimal
            message[i][j] = sbox[int(hexadecimal[0], 16)][int(hexadecimal[1], 16)]
    return message
    # TODO: Check if returns in decimal or hexadecimal

def __shift_rows(message):
    """
        Rotates 2nd, 3rd and 4th row of matrix, each by different amount.
        This rotation is done by using list slicing.
    """
    for i in range(4):
        message[i] = message[i:] + message[:i]
    return message

# 'state_mat' is the main State matrix, 'temp_mat' is a temp matrix of the same dimensions as 'state_mat'.
def __mix_columns(state_mat):
    """
        mix_columns
    """
    g_mul = __g_mul
    temp_mat = [[]] # Array.Clear(temp_mat, 0, temp_mat.Length);

    for column in range(4):
        temp_mat[0][column] = (g_mul(0x02, state_mat[0][column]) ^ g_mul(0x03, state_mat[1][column]) ^ state_mat[2][column] ^ state_mat[3][column])
        temp_mat[1][column] = (state_mat[0][column] ^ g_mul(0x02, state_mat[1][column]) ^ g_mul(0x03, state_mat[2][column]) ^ state_mat[3][column])
        temp_mat[2][column] = (state_mat[0][column] ^ state_mat[1][column] ^ g_mul(0x02, state_mat[2][column]) ^ g_mul(0x03, state_mat[3][column]))
        temp_mat[3][column] = (g_mul(0x03, state_mat[0][column]) ^ state_mat[1][column] ^ state_mat[2][column] ^ g_mul(0x02, state_mat[3][column]))

    state_mat = temp_mat # temp_mat.CopyTo(s, 0);
    return state_mat

def __g_mul(a, b):
    """
        g_mul, Bitwise multiplication
    """
    result = 0
    for i in range(8):
        if ((b & 1) != 0):
            result ^= a
        hi_bit_set = (a & 0x80)
        a <<= 1
        if (hi_bit_set != 0):
            a ^= 0x1b # Polynomial x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return result

def __message_fusion(message):
    result_string = ""
    for i in range(4):
        for j in range(4):
            letter = chr(message[i][j])
            result_string += letter
    return result_string

