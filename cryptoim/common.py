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

def __key_expansion(key):
    """
        key_expansion
    """
    import hashlib
    extendedkey = ''
    keyhash = key       # Assigns key value to the keyhash, for later use in cycle
    for _ in range(32):
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
            for _ in range(4):
                # Converts letter to decimal number
                decimal = ord(extendedkey[k])
                # Appends 4 numbers into each row of matrix
                roundkey[i].append(decimal)
                k += 1
        roundkeys.append(roundkey)
    return roundkeys

def __add_roundkey(message, roundkey):
    """
        add_roundkey
    """
    # Uses one matrix of each as input
    for i in range(4):
        for j in range(4):
            message[i][j] = message[i][j]^roundkey[i][j] # XOR
    return message

def __convert_char_hex(message_char):
    """
        convert_char_hex
    """
    hex_str = hex(message_char)[2:]
    if len(hex_str) % 2 == 1:
        hex_str = '0' + hex_str
    return hex_str
