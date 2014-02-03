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

import cryptoim.decryptor_core as decryptor_core
from tests.unit.common import *

from nose.tools import ok_, eq_

def test_decrypt():

    decrypt = decryptor_core.decrypt

    message = 'This is a test message'
    ciphertext = '5fec00953baae86a9b99796be672edcef8e893a9882c55ba29661d1ab62efa45' # manually encrypted
    key = 'This is a test key'
    plaintext = decrypt(ciphertext, key)
    eq_(message, plaintext)

def test_ciphertext_fission():

    ciphertext_fission = decryptor_core.__ciphertext_fission

    ctext = '969afe5697ae7805308929daeb94c65b6e85768bc40dccd4bc616dd7345e6ec6'
    ciphertexts = ciphertext_fission(ctext)
    for cts in ciphertexts:
        eq_(len(cts), 4)
        for row in cts:
            eq_(len(row), 4)


def test_rsub_bytes():

    rsub_bytes = decryptor_core.__rsub_bytes

    input_mat = [[0x00, 0x01, 0x02, 0x03],
                 [0xab, 0xcd, 0xef, 0xff],
                 [0x1a, 0x2b, 0x3c, 0x4d],
                 [0x2c, 0xe1, 0x12, 0x3a]]

    # Manually subbed using encryptor_core.__sub_bytes
    subbed_mat = [[82, 9, 106, 213],
                  [14, 128, 97, 125],
                  [67, 11, 109, 101],
                  [66, 224, 57, 162]]

    eq_(input_mat, rsub_bytes(subbed_mat))

def test_rshift_rows():

    rshift_rows = decryptor_core.__rshift_rows

    input_mat = [[1, 2, 3, 4],
                 [2, 3, 4, 1],
                 [3, 4, 1, 2],
                 [4 ,1, 2, 3]]
    expected_mat = [[1, 2, 3, 4],
                    [1, 2, 3, 4],
                    [1, 2, 3, 4],
                    [1, 2, 3, 4]]
    eq_(rshift_rows(input_mat), expected_mat)
