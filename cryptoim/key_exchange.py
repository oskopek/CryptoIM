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
    rnd = generate_random(0, len(PRIMES))
    return PRIMES[rnd]

def base_pick():
    """
        Returns a random number from the const.PRIMES array from indexes interval (0, 15)
    """
    rnd = generate_random(1, 15)
    return rnd

def make_public_key(prime, base, rnumber):
    """
        Returns (base^number) mod prime, the public key used for the key exchange
    """
    pub_key = (base ** rnumber) % prime
    return pub_key

def make_final_key(prime, pub_key, p_number):
    """
        Returns (pub_key^p_number) mod prime, the key used for encryption
    """
    private_key = (pub_key ** p_number) % prime
    return private_key
