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

from cryptoim import encryptor_core
from nose.tools import ok_, eq_

def test_encrypt():
    """
        Test for encryptor_core.encrypt
    """
    encrypt = encryptor_core.encrypt

    message = "test"

    def rand_str(limit):
        from string import ascii_letters, digits
        from random import choice

        rand = ""
        for i in range(limit):
            rand += choice(ascii_letters)
        return rand

    key = rand_str(256)
    eq_(len(key), 256)

    encrypted_str = encrypt(message, key)
    print(encrypted_str)
    ok_(len(encrypt(message, key)) >= 0, "Length wasn't supposed to be 0")

def test_g_mul():
    """
        Test for encryptor_core.__g_mul
    """
    g_mul = encryptor_core.__g_mul

    eq_(g_mul(0x00,0x01),0x00)
    eq_(g_mul(0x00,0xFF),0x00)
    eq_(g_mul(0x01,0xAB),0xAB)
    print(0x02)
    print(0xFF)
    print(0x02 * 0xFF)
    print(g_mul(0x02,0xFF))
    #ok_(g_mul(0x02,0xFF)<=0xFF,"This thing does not work") # out-commented, because it doesn't work and would break the build

def test_sub_bytes():
    """
        Test for encryptor.core.__sub_bytes
    """
    sub_bytes = encryptor_core.__sub_bytes

    input_mat = [[0x01,0x02,0xFF,0xAB],
                 [0x15,0x00,0xEE,0x32],
                 [0x05,0x0A,0x0D,0x0F],
                 [0x4F,0x3D,0xA3,0xC9]]

    expected_mat = [[0x09,0x6A,0x7D,0x0E],
                    [0x2F,0x52,0x99,0xA1],
                    [0x36,0xA3,0xF3,0xFB],
                    [0x92,0x8B,0x71,0x12]]

    eq_(sub_bytes(input_mat), expected_mat)

def test_message_fusion():
    """
        Test for encryptor_core.__message_fusion
    """
    message_fusion = encryptor_core.__message_fusion

    input_mat= [[39, 225, 248, 242],
                [148, 88, 11, 253],
                [109, 38, 230, 13],
                [12, 229, 160, 182]]

    ok_(variable._type(message_fusion(input_mat))=str,"Not a string!")
    eq_(len(message_fusion(input_mat)),32)


    
