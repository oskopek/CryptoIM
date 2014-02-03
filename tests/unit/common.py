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

import random, string

def random_string_range(lo, hi):
    """
        Returns a random string of string.printable characters, of length randint(lo, hi)
    """

    length = random.randint(lo, hi)
    return ''.join(random.choice(string.printable) for _ in range(length))

def random_string_length(length):
    """
        Returns a random string of string.printable characters, of the given length
    """

    return random_string_range(length, length)

def random_string_limit(limit):
    """
        Returns a random string of string.printable characters, of length randint(1, limit)
    """

    return random_string_range(1, limit)
