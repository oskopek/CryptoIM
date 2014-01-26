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

import cryptoim.key_exchange as k_ex
from nose.tools import ok_, eq_

def test_generate_random():
    """
        Test for key_exchange.generate_random
    """
    generate_random = k_ex.generate_random
    
    random_numero = generate_random(1, 100)
    eq_(type(random_numero), int or long)
    ok_(random_numero >= 1 and random_numero <= 100)

def test_prime_pick():
    """
        Test for key_exchange.prime_prick
    """
    prime_pick = k_ex.prime_pick

    prime = prime_pick()
    eq_(type(prime), int)

def test_base_pick():
    """
        Test for key_exchange.base_pick
    """
    base_pick = k_ex.base_pick

    base = base_pick()
    eq_(type(base), int)

def test_make_public_key():
    """
        Test for key_exchange.make_public_key
    """
    make_public_key = k_ex.make_public_key
    prime_pick = k_ex.prime_pick
    generate_random = k_ex.generate_random
    base_pick = k_ex.base_pick
    
    prime = prime_pick()
    base = base_pick()
    rnumber = generate_random(1, 100)
    
    public_key = make_public_key(prime, base, rnumber)
    manual_public_key = (base**rnumber)%prime
    
    ok_(type(public_key) == int or type(public_key) == long)
    eq_(public_key, manual_public_key)

def test_make_final_key():
    """
        Test for key_exchange.make_final_key
    """
    make_public_key = k_ex.make_public_key
    prime_pick = k_ex.prime_pick
    generate_random = k_ex.generate_random
    base_pick = k_ex.base_pick
    make_final_key = k_ex.make_final_key

    for i in range(100):
        a = generate_random(1, 100)
        b = generate_random(1, 100)
        p = prime_pick()
        g = base_pick()
    
        A = make_public_key(p, g, a)
        B = make_public_key(p, g, b)
        
        ok_(type(make_final_key(p, B, a)) == int or type(make_final_key(p, B, a)) == long)
        ok_(type(make_final_key(p, A, b)) == int or type(make_final_key(p, A, b)) == long)   
        eq_(make_final_key(p, B, a), make_final_key(p, A, b))

