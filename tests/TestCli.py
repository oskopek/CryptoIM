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

def test_connect_disconnect():

    cshell = CryptoShell('main.cfg')
    cshell.test_mode = True
    eq_(cshell.do_connect(''), False)
    eq_(cshell.do_connect('cryptoim1'), True)
    eq_(cshell.do_connect('cryptoim1'), False)
    eq_(cshell.do_disconnect(''), True)
    eq_(cshell.do_disconnect(''), False)
    eq_(cshell.do_connect('cryptoim1@jabber.de crypto_test'), True)
    eq_(cshell.do_disconnect(''), True)
    eq_(cshell.do_disconnect(''), False)

def test_send():

    cshell = CryptoShell('main.cfg')
    cshell.test_mode = True
    eq_(cshell.do_send('message before connection'), False)
    eq_(cshell.do_connect('cryptoim2'), True)
    TestXMPP.waitForSession(cshell.xmpp_client, True)
    eq_(cshell.do_send(''), False)
    eq_(cshell.do_send('shouldntwork message'), False)
    eq_(cshell.do_send('cryptoim1 message'), True)
    eq_(cshell.do_send('cryptoim1'), False)
    cshell.do_disconnect('')

def test_chat_stopchat_exit():

    cshell = CryptoShell('main.cfg')
    cshell.test_mode = True
    eq_(cshell.do_chat(''), False)
    eq_(cshell.do_chat('cryptoim1@jabber.de'), True)
    eq_(cshell.do_chat('cryptoim1'), True)
    eq_(cshell.do_chat('shouldntwork'), False)
    eq_(cshell.do_connect('cryptoim2'), True)
    TestXMPP.waitForSession(cshell.xmpp_client, True)
    eq_(cshell.do_send('Test message'), True)
    eq_(cshell.do_s('Test message for short version'), True)
    eq_(cshell.do_stopchat(''), True)
    eq_(cshell.do_stopchat(''), False)
    eq_(cshell.do_send('Test message after stopchat'), False)
    eq_(cshell.do_s('Alsto testing the short version'), False)
    cshell.do_disconnect('')

    exit_code = -1
    try:
        cshell.do_q('')
    except SystemExit:
        exit_code = 0
    eq_(0, exit_code)


def test_addfriend_removefriend():

    cshell = CryptoShell('tests/test_config.cfg')
    cshell.test_mode = True

    eq_(cshell.do_addfriend('testfriend testfriend@jabber.de'), True)
    eq_(cshell.do_addfriend('testfriend testfriend@jabber.de'), False)
    eq_(cshell.do_addfriend(''), False)
    eq_(cshell.do_removefriend('testfriend'), True)
    eq_(cshell.do_removefriend('testfriend another few lines'), False)
    eq_(cshell.do_removefriend(''), False)
    eq_(cshell.do_removefriend('testfriend'), False)

def test_addconnection_removeconnection():
    
    cshell = CryptoShell('tests/test_config.cfg')
    cshell.test_mode = True

    eq_(cshell.do_addconnection('testuser2 testuser2@jabber.de testpass'), True)
    eq_(cshell.do_addconnection('testuser2 testuser2@jabber.de testpass'), False)
    eq_(cshell.do_addconnection('testuser2'), False)
    eq_(cshell.do_addconnection('testuser2 thisisnotajid testpass'), False)
    eq_(cshell.do_removeconnection('testuser3'), False)
    eq_(cshell.do_removeconnection('testuser2 testuser3@jabber.de'), False)
    eq_(cshell.do_removeconnection('testuser2@jabber.de'), False)
    eq_(cshell.do_removeconnection('testuser2'), True)




