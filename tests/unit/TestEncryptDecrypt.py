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
import cryptoim.decryptor_core as decryptor_core
from tests.unit.common import *

from nose.tools import ok_, eq_

def test_random_encrypt_decrypt():

    test_count = 10
    limit = 100

    for _ in range(test_count):
        originaltext = random_string_limit(limit)
        key = random_string_limit(limit)

        ciphertext = encryptor_core.encrypt(originaltext, key)
        check_decrypt(originaltext, ciphertext, key)

def check_decrypt(originaltext, ciphertext, key):

    decryptedtext = decryptor_core.decrypt(ciphertext, key)
    eq_(originaltext, decryptedtext)

def test_random_key():

    length = 100
    originaltext = 'Secret message!'
    key = random_string_length(length)
    ciphertext = encryptor_core.encrypt(originaltext, key)
    check_decrypt(originaltext, ciphertext, key)

def test_long_string():

    length = 1000
    originaltext = random_string_length(length)
    key = 'This is a secret key!'
    ciphertext = encryptor_core.encrypt(originaltext, key)
    check_decrypt(originaltext, ciphertext, key)
