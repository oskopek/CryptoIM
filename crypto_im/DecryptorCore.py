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

def decrypt (private_key, ciphertext):

    def makeroundkey (key1, key2, strings):
        #a = 1
        #b = 2
        RoundKeys = []
        #Default Values

        key1 = int(key1, 16)
        key2 = int(key2, 16)
        #Formats key values into bin int

        for i in range(16):
            strings[i] = int(strings[i].encode("hex"), 16)
        #Puts strings into hex

        for i in range (16):
            if i %2 == 0:
                RoundKeys.append(key2^strings[i])
            elif i %2 == 1:
                RoundKeys.append(key1^strings[i])
            else:
                RoundKeys.append(key2^strings[i])
        #Sorts RoundKeys in right order
        return RoundKeys
        #Returns list of RoundKeys(16 RoundKeys)

    messages = []
    keys = []

    ciphertext = ciphertext.split(",") #Converts string into list
    for i in range (len (ciphertext)):
        if i % 2 == 0 or i % 2 == 2:
            messages.append(ciphertext[i])
        if i % 2 == 1:
            keys.append(ciphertext[i])
##    For every odd i adds to keys value
##    from ciphertexts on position i and
##    for every even i adds value to
##    messages from ciphertexts on pos. i

    for i in range (len(messages)):
        while len(messages[i])<16:
            "0" + messages[i]


    for i in range(len(keys)):
        while len(keys[i]) < 16:
            "0" + keys[i]
        keys[i] = int(keys[i], 16)

##    Fixes lengths of keys and messages
##    in case that they fail

    private_key = int(private_key, 16)
    #Prepares private key to xor

    for w in range (len(messages)):
        key = private_key^keys[w]
        #Decrypts the key used for particular message

        key = hex(key)
        key = key.lstrip("0x").rstrip("L")
        #Convers keys to hexadecimal value
        while len(key)<16:
            key = "0" + key
        #Corrects possible length loss

        k1 = ""
        k2 = ""
        for i in range (8):
            k1 = k1 + key[i]
            k2 = k2 + key[i+8]
##        Splits the key into 2 smaller keys
##        Original length of key was 64 bits
##        = 16 hex, since original length of
##        key was 64 bits, new length must
##        correspond (no need to correct this)

        RoundStrings = ["aeio", "chjm", "l0qd", "z4kh", "u4wr",
        "ctel", "afja", "is2x", "svgw", "hv2j", "jkds", "sv;s",
        "29ce", "v29f", "ajf9", "xiw2"]

##        Roundstrings are fixed to create roundkeys
##        They are put into loop so their value does
##        not overwrite with every round

        RoundKeys = makeroundkey(k1, k2, RoundStrings)


        Left = []
        Right = []
        Output = []
        #Prepares empty arrays for Feistel Network
        m1 = ""
        m2 = ""
##        Prepares empty strings for input values of m1
##        and m2 which have to be separated into 2 halfs
##        due to their length which is 64 bits and Feistel
##        input is 32 bits on each side

        m1 = m1 + messages[w][:8]
        m2 = m2 + messages[w][8:]
        #Splits the messages
        print m1
        print m2
        print RoundKeys
        for x in range(17):
            if x == 0:
                Right.append(int(m2, 16))
                Left.append(int(m1, 16))
            else:
                Right.append(Left[x-1])
                Left.append((Right[x-1]^RoundKeys[16-x])^Left[x-1])
        Left[16] = hex(Left[16]).lstrip("0x").rstrip("L")
        Right[16] = hex(Right[16]).lstrip("0x").rstrip("L")
        print Left[16]
        print Right[16]
        Output.append (Left[16]+Right[16])
        print Output
        Output[w] = Output[w].decode("hex")
        return Output
