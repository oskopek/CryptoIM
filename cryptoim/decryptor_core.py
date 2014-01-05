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

from cryptoim import encryptor_core

def decrypt(ciphertext, key):
    """
        decrypt
    """
    print(ciphertext, key)

def __ciphertext_fission(ciphertext):
    """
        Ciphertext splitter, splits ciphertext, and puts chunks into matrices
        which are then put into list.
    """
    assert len(ciphertext) % 2 == 0

    ciphertext = []
    hexadecimal = ''

    for _ in range((len(ciphertext)/32 + 1)):
        matrix = [[], [], [], []]
        for i in range(32):
            hexadecimal += ciphertext[i]
            if len(hexadecimal) == 2:
                matrix[i/8].append(int(hexadecimal, 16))
            ciphertext.append(matrix)
    return ciphertext

def __mat_search(mat, elem):
    """
        Mat Search, returns tuple (row, column)
    """
    for i in range(len(mat)):
        try:
            mat[i].index(elem)
            return i, mat[i].index(elem)
        except ValueError:
            print('Expected ValueError')

def __rsub_bytes(ciphertext):
    chex = encryptor_core.__convert_char_hex
    """
        Reversed SubBytes step
    """
    for i in range(4):
        for j in range(4):
            idx = __mat_search(encryptor_core.SBOX, ciphertext[i][j])
            ciphertext[i][j] = int((chex(idx[0]) + chex(idx[1])), 16)
    return ciphertext

def __rshift_rows(ciphertext):
    """
        Reversed shift rows
    """
    for i in range(4):
        ciphertext[i] = ciphertext[i][-i:] + ciphertext[i][:-i]
    return ciphertext

