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

from cryptoim.cli import CryptoShell

from nose.tools import ok_, eq_, nottest
import time


def test_connect_disconnect():

    cshell = CryptoShell('main.cfg')
    eq_(cshell.do_connect(''), False)
    eq_(cshell.do_connect('cryptoim1'), True)
    eq_(cshell.do_connect('cryptoim1'), False)
    eq_(cshell.do_disconnect(''), True)
