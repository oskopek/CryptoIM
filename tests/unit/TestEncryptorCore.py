#!/usr/bin/env python
# encoding: utf-8

"""
   Copyright 2014 CryptoIM Development Team

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

import cryptoim.encryptor_core as encryptor_core
from tests.unit.common import *

from nose.tools import ok_, eq_

def test_encrypt():

    encrypt = encryptor_core.encrypt

    message = 'This is a test message'
    encrypted_message = '5fec00953baae86a9b99796be672edcef8e893a9882c55ba29661d1ab62efa45' # manually encrypted
    key = 'This is a test key'
    ciphertext = encrypt(message, key)
    eq_(encrypted_message, ciphertext)

def test_g_mul():

    g_mul = encryptor_core.__g_mul

    eq_(g_mul(0x01, 0x02), 0x02)
    eq_(g_mul(0xFF, 0x03), 0x1a)

def test_sub_bytes():

    sub_bytes = encryptor_core.__sub_bytes

    input_mat = [[0x01, 0x02, 0xFF, 0xAB],
                 [0x15, 0x00, 0xEE, 0x32],
                 [0x05, 0x0A, 0x0D, 0x0F],
                 [0x4F, 0x3D, 0xA3, 0xC9]]

    expected_mat = [[0x09, 0x6A, 0x7D, 0x0E],
                    [0x2F, 0x52, 0x99, 0xA1],
                    [0x36, 0xA3, 0xF3, 0xFB],
                    [0x92, 0x8B, 0x71, 0x12]]

    eq_(sub_bytes(input_mat), expected_mat)

def test_message_fusion():

    message_fusion = encryptor_core.__message_fusion

    input_mat = [   [39, 225, 248, 242],
                    [148, 88, 11, 253],
                    [109, 38, 230, 13],
                    [12, 229, 160, 182]]

    input_mat_zeros = [[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]

    ok_(type(message_fusion(input_mat)) == str, 'Not a string!')
    ok_(type(message_fusion(input_mat_zeros)) == str, 'Zeros - Not a string!')
    eq_(len(message_fusion(input_mat)), 32)
    eq_(len(message_fusion(input_mat_zeros)), 32)

def test_key_expansion():

    key_expansion = encryptor_core.__key_expansion

    def rand_str(limit):
        """
            rand_str
        """
        from string import ascii_letters
        from random import choice

        rand = ''
        for _ in range(limit):
            rand += choice(ascii_letters)
        return rand

    key = rand_str(32)
    eq_(len(key_expansion(key)), 256)

def test_mix_columns():

    mix_columns = encryptor_core.__mix_columns

    input_mat = [[0xdb, 0xf2, 0xd4, 0x2d],
                 [0x13, 0x0a, 0xd4, 0x26],
                 [0x53, 0x22, 0xd4, 0x31],
                 [0x45, 0x5c, 0xd5, 0x4c]]

    expected_mat = [[0x8e, 0x9f, 0xd5, 0x4d],
                    [0x4d, 0xdc, 0xd5, 0x7e],
                    [0xa1, 0x58, 0xd7, 0xbd],
                    [0xbc, 0x9d, 0xd6, 0xf8]]
    eq_(mix_columns(input_mat), expected_mat)
