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
    """
    Returns list of 16 matrices, these are 128 bit roundkeys used for encryption,
    from there 16 matrices will be only 14 used. For opimization purpose was used
    index k instead of another cycle.
    """
        k = 0
        roundkeys = []
        for k in range(16):
            roundkey = [[],[],[],[]] #Matrix (list of lists)
            for i in range(4):
                for j in range(4): 
                    hexadecimal = int(hex(ord(extendedkey[k])),16) #Converts letter to decimal number
                    roundkey[i].append(hexadecimal)#Appends 4 numbers into each row of matrix
                    k += 1
            roundkeys.append(roundkey)
        return roundkeys

    def SplitMessage(plaintext):
    """
    Splits message into 128 bits (16 characters) chunks and each of these
    chunks is then transformed into matrix with decimal value. These matrices
    are stored into list, creating a list of matrices.
    """
    messsage_chunks = []
    message_chunk = ''
    for character in plaintext:
        message_chunk += character
        if len(message_chunk) == 16: #After 16 characters appends 1 chunk into a list of chunks
            message_chunks.append(message_chunk)
            message_chunk = ''
    messages = []
    for i in range(len(message_chunks)):
        matrix = [[],[],[],[]]
        for j in range(4):
            for k in range(4):
                number = int(hex(ord(message_chunks[4*i+j])),16) #Cool way to iterate and transform at the same time
                matrix[j].append(number)
        messages.append(matrix)
    return messages
    """
    TODO: Check if this works as expected
    """
            
        
    
