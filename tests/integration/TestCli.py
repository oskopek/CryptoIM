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
import cryptoim.cli as cli
from tests.integration import TestXMPP

from nose.tools import ok_, eq_

def test_connect_disconnect():

    cshell = CryptoShell('main.cfg')
    cshell.test_mode = True
    eq_(cshell.do_connect(''), False)
    eq_(cshell.do_connect('invalid number of arguments'), False)
    eq_(cshell.do_connect('cryptoim'), True)
    eq_(cshell.do_connect('cryptoim'), False)
    eq_(cshell.do_disconnect('random_string'), True) # branch coverage
    eq_(cshell.do_disconnect(''), False)

    exit_code = -1
    try:
        cshell.do_q('')
    except SystemExit:
        exit_code = 0
    eq_(0, exit_code)

def test_connect_disconnect_jid():

    cshell = CryptoShell('main.cfg')
    cshell.test_mode = True
    eq_(cshell.do_connect('cryptoim@jabber.de/random_resource_gets_stripped crypto_test'), True)
    eq_(cshell.do_disconnect(''), True)
    eq_(cshell.do_disconnect(''), False)

def test_send():

    cshell = CryptoShell('main.cfg')
    cshell.test_mode = True
    eq_(cshell.do_send('cryptoim message before connection'), False)
    eq_(cshell.do_connect('cryptoim2'), True)
    TestXMPP.waitForSession(cshell.messenger, True)
    eq_(cshell.do_send(''), False)
    eq_(cshell.onecmd(''), None) # just empty line command - emptyline() test
    eq_(cshell.do_send('shouldntwork message'), False)
    eq_(cshell.do_send('cryptoim message'), True)
    eq_(cshell.do_send('cryptoim2@jabber.de message'), True)
    eq_(cshell.do_send('cryptoim'), False)
    cshell.do_disconnect('')

def test_chat_closechat_exit():

    cshell = CryptoShell('main.cfg')
    cshell.test_mode = True
    eq_(cshell.do_chat(''), False)
    eq_(cshell.do_chat('cryptoim@jabber.de'), True)
    eq_(cshell.do_chat('cryptoim'), True)
    eq_(cshell.do_chat('shouldntwork'), False)
    eq_(cshell.do_connect('cryptoim2'), True)
    TestXMPP.waitForSession(cshell.messenger, True)
    eq_(cshell.do_send('Test message'), True)
    eq_(cshell.do_s('Test message for short version'), True)
    eq_(cshell.do_send(''), False)
    eq_(cshell.do_closechat(''), True)
    eq_(cshell.do_closechat(''), False)
    eq_(cshell.do_send('Test message after stopchat'), False)
    eq_(cshell.do_s('Alsto testing the short version'), False)
    cshell.do_disconnect('')

    exit_code = -1
    try:
        cshell.do_exit('')
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
    eq_(cshell.do_addconnection('testuser3'), False)
    eq_(cshell.do_addconnection('testuser3 thisisnotajid testpass'), False)
    eq_(cshell.do_removeconnection('testuser3'), False)
    eq_(cshell.do_removeconnection('testuser2 testuser3@jabber.de'), False)
    eq_(cshell.do_removeconnection('testuser2@jabber.de'), False)
    eq_(cshell.do_removeconnection('testuser2'), True)

def test_friendlist():

    cshell = CryptoShell('main.cfg')
    cshell.test_mode = True
    eq_(cshell.do_friendlist(''), None)
    eq_(cshell.do_friendlist('whatever string'), None)

def test_return_cli():

    cshell = CryptoShell('tests/test_config.cfg')
    cshell.test_mode = True
    eq_(cshell.return_cli(False), False)
    eq_(cshell.return_cli(True), True)
    eq_(cshell.return_cli('test'), 'test')
    eq_(cshell.return_cli(123), 123)
    cshell.test_mode = False
    eq_(cshell.return_cli(False), None)
    eq_(cshell.return_cli(True), None)
    eq_(cshell.return_cli('test'), None)
    eq_(cshell.return_cli(123), None)

def test_create_config():
    config_file = 'tests/test_config_nonexistant.cfg'
    cshell = CryptoShell(config_file)
    import os
    os.remove(config_file)

# Test tools
def test_sanit_is_jid():
    is_jid = cli.sanit_is_jid
    eq_(True, is_jid('test@jabber.de'))
    eq_(True, is_jid('test@jabber.de/resourceHere123'))
    eq_(True, is_jid('test@localhost'))
    eq_(True, is_jid('tes1234tBigSmall@jabber.DE'))

    eq_(False, is_jid('testjabber.de'))
    eq_(False, is_jid('test/jabber@de'))
    eq_(False, is_jid('test&jabber.de'))
    eq_(False, is_jid('test@jabber&de'))
    eq_(False, is_jid('te@st@jabber.de'))
    eq_(False, is_jid('test@jabber..de'))
    eq_(False, is_jid('te.st@jabber.de'))
    eq_(False, is_jid('te&st@jabber.de'))
    eq_(False, is_jid('test@jabber.de/resourceHere.123'))
    eq_(False, is_jid('test@jabber.de/resource&&Here123'))
