#!/usr/bin/env python
# encoding: utf-8

"""
   Copyright 2013,2014 CryptoIM Development Team

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

def Encrypt(plaintext,key):
"""
plaintext = string
key = string (256 bytes)
"""
    def KeyExpansion(key):
        import hashlib
        extendedkey = ''
        keyhash = key       #Assigns key value to the keyhash, for later use in cycle
        for i in range(32):
            keyhash = hashlib.sha224(keyhash.encode('utf-8')).hexdigest()
            extendedkey += keyhash
        extendedkey = extendedkey[:256]
        return extendedkey

    def RoundKeySeparator(extendedkey):
        k = 0
        roundkeys = []
        for i in range(16):
            roundkey = [[],[],[],[]] #Matrix (list of lists)
            for i in range(4):
                for j in range(4):
                    hexadecimal = int(hex(ord(extendedkey[k])),16) #Converts letter to decimal number
                    roundkey[i].append(hexadecimal)
                    k += 1
            roundkeys.append(roundkey)
        return roundkeys

"""
Returns list of 16 matrices, these are 128 bit roundkeys used for encryption,
from there 16 matrices will be only 14 used. For opimization purpose was used
index k instead of another cycle.
"""
    
