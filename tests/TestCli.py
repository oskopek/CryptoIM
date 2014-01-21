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
import TestXMPP

from nose.tools import ok_, eq_

# TODO redo cli tests without returns

def test_connect_disconnect():

    cshell = CryptoShell('main.cfg')

    cshell.do_connect('')
    #eq_(False, cshell.xmpp_client.is_connected())

    cshell.do_connect('cryptoim1')
    eq_(True, cshell.xmpp_client.is_connected())

    cshell.do_connect('cryptoim1')
    eq_(True, cshell.xmpp_client.is_connected())

    cshell.do_disconnect('')
    eq_(False, cshell.xmpp_client.is_connected())

    cshell.do_disconnect('')
    eq_(False, cshell.xmpp_client.is_connected())

def test_send():

    cshell = CryptoShell('main.cfg')
    cshell.do_connect('cryptoim2')
    eq_(True, cshell.xmpp_client.is_connected())
    TestXMPP.waitForSession(cshell.xmpp_client, True)
    eq_(True, cshell.xmpp_client.is_in_session())
    #eq_(cshell.do_send(''), False)
    #eq_(cshell.do_send('shouldntwork message'), False)
    #eq_(cshell.do_send('cryptoim1 message'), True)
    #eq_(cshell.do_send('cryptoim1'), False)
    cshell.do_disconnect('')
    eq_(False, cshell.xmpp_client.is_connected())
