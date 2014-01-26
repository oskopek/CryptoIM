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

import random
from cryptoim.const import PRIMES

# Random generator useable for cryptography
RAND = random.SystemRandom()

def generate_random(limit_lo, limit_hi):
    """
        Returns a random integer inside the (limit_lo, limit_hi) interval
    """
    return RAND.randint(limit_lo, limit_hi)

def prime_pick():
    """
        Returns a random number from the const.PRIMES array
    """
    rnd = generate_random(0, len(PRIMES) - 1)
    return PRIMES[rnd]

def base_pick():
    """
        Returns a random number from the const.PRIMES array from indexes interval (0, 15)
    """
    rnd = generate_random(2, 15)
    return rnd

def make_public_key(prime, base, rnumber):
    """
        Returns (base^number) mod prime, the public key used for the key exchange
    """
    pub_key = (base ** rnumber) % prime
    return pub_key

def make_final_key(prime, public, private):
    """
        Returns (pub_key^p_number) mod prime, the key used for encryption
    """
    key = (public ** private) % prime
    return key

def encode_syn(prime, base, A):
    """
        Encodes the numbers in a standardized format
    """
    return 'SYN;%i;%i;%i' % (prime, base, A)

def decode_syn(msg):
    """
        Decodes the numbers in a standardized format
    """
    cut = msg[4:] # Omit the first 4 chars ('SYN;')
    spl = cut.split(';')
    prime = int(spl[0])
    base = int(spl[1])
    A = int(spl[2])
    return prime, base, A

def encode_ack(B):
    """
        Encodes the number in a standardized format
    """
    return 'ACK;%i' % (B)

def decode_ack(msg):
    """
        Decodes the number in a standardized format
    """
    cut = msg[4:] # Omit the first 4 chars ('ACK;')
    return int(cut)
