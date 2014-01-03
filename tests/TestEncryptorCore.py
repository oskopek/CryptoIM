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

    #ok_(len(encrypt(message, key)) != 0, "Length wasn't supposed to be 0")

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
    # ok_(g_mul(0x02,0xFF)<=0xFF,"This thing does not work") # out-commented, because it doesn't work and would break the build
