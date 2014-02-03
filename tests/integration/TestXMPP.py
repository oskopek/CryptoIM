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

import cryptoim.xmpp as xmpp
from cryptoim.cli import CryptoShell

from nose.tools import ok_, eq_, nottest
import time

def init_xmpp_clients():
    """
        Initializes the xmpp_clients and connects them
    """
    crypto_shell = CryptoShell('main.cfg')

    xmpp_client = xmpp.XMPPClient('cryptoim@jabber.de', 'crypto_test', crypto_shell)
    xmpp_client.connect_server(should_block=False)

    crypto_shell2 = CryptoShell('main.cfg')
    xmpp_client2 = xmpp.XMPPClient('cryptoim2@jabber.de', 'crypto_test2', crypto_shell2)
    xmpp_client2.connect_server(should_block=False)

    waitForConnection(xmpp_client, True)
    waitForConnection(xmpp_client2, True)
    return xmpp_client, xmpp_client2

def test_connect():
    """
        Test for xmpp.XMPPClient.connect_server and disconnect_server
    """
    xmpp_client, xmpp_client2 = init_xmpp_clients()
    eq_(xmpp_client.is_connected(), True)
    eq_(xmpp_client2.is_connected(), True)

    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)
    xmpp_client2.disconnect_server()
    waitForConnection(xmpp_client2, False)

def test_send_message():
    """
        Test for xmpp.XMPPClient.send_message
    """
    xmpp_client, xmpp_client2 = init_xmpp_clients()
    crypto_shell = xmpp_client.xmpp.parent
    waitForConnection(xmpp_client, True)
    waitForConnection(xmpp_client2, True)
    waitForSession(xmpp_client, True)
    waitForSession(xmpp_client2, True)
    msg = 'Hello, CryptoIM check_send_message!'
    recipient = xmpp_client2.xmpp.boundjid.full
    xmpp_client.send_message(recipient, msg)

    waitForNonEmptyList(crypto_shell.sent_msg_list)

    xmpp_client.disconnect_server()
    xmpp_client2.disconnect_server()
    waitForConnection(xmpp_client, False)
    waitForConnection(xmpp_client2, False)

    # Assert that xmpp_client sent the message (it is bound to be sent after disconnect if it waits)   
    ok_(1 == len(crypto_shell.sent_msg_list))
    eq_(len(crypto_shell.sent_jid_list), len(crypto_shell.sent_msg_list))
    eq_(msg, crypto_shell.sent_msg_list[-1])
    eq_(recipient, crypto_shell.sent_jid_list[-1])

def test_not_connect():
    """
        Failproofing test for xmpp.XMPPClient.connect_server and disconnect_server
    """

    crypto_shell = CryptoShell('main.cfg')

    # Wrong host
    xmpp_client = xmpp.XMPPClient('cryptoim@jabber2.de', 'crypto_test', crypto_shell)
    assertDisconnect(xmpp_client)


    # Wrong pass
    xmpp_client = xmpp.XMPPClient('cryptoim@jabber.de', 'wrong_pass', crypto_shell)
    assertDisconnect(xmpp_client)

    # Wrong name
    xmpp_client = xmpp.XMPPClient('cryptoim0@jabber.de', 'crypto_test', crypto_shell)
    assertDisconnect(xmpp_client)

def assertDisconnect(xmpp_client):
    """
        Conencts, disconnects and asserts it happened
    """
    xmpp_client.connect_server(should_block=False, should_reattempt=False)

    waitForConnection(xmpp_client, False)

    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)

def test_receive_message():
    """
        Test for CryptoXMPP.message (receive message)
    """
    xmpp_client, xmpp_client2 = init_xmpp_clients()
    crypto_shell2 = xmpp_client2.xmpp.parent

    # Assert connected
    waitForConnection(xmpp_client, True)
    waitForConnection(xmpp_client2, True)
    waitForSession(xmpp_client, True)
    waitForSession(xmpp_client2, True)

    # Send and receive message
    plaintext = 'Hello, CryptoIM check_receive_message!'
    xmpp_client.xmpp.send_message(mto = xmpp_client2.xmpp.boundjid.full, mbody = 'test', mtype = 'error') # Test for dropping non-chat messages
    ciphertext = xmpp_client.send_message(xmpp_client2.xmpp.boundjid.full, plaintext)

    waitForNonEmptyList(crypto_shell2.received_msg_list)

    # Disconnect
    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)
    xmpp_client2.disconnect_server()
    waitForConnection(xmpp_client2, False)

    # Assert that xmpp_client2 got it (it is bound to be received after disconnect if it waits)
    print(('Received msg list: ', crypto_shell2.received_msg_list))
    print(('Received jid list: ', crypto_shell2.received_jid_list))

    ok_(1 == len(crypto_shell2.received_msg_list))
    eq_(len(crypto_shell2.received_jid_list), len(crypto_shell2.received_msg_list))
    eq_(plaintext, crypto_shell2.received_msg_list[-1])
    eq_(xmpp_client.xmpp.boundjid.full, crypto_shell2.received_jid_list[-1])

# Test tools

def waitForNonEmptyList(lst):
    counter = 0
    while len(lst) < 1:
        if counter > 100: break #10 secs
        time.sleep(0.1)
        counter += 1
    ok_(len(lst) > 0)

def waitForConnection(xmpp_client, should_be_connected):
    """
        Waits until a connection is estabilished
    """
    while not xmpp_client.is_connected() == should_be_connected:
        time.sleep(0.1)
    eq_(xmpp_client.is_connected(), should_be_connected)

def waitForSession(xmpp_client, should_be_in_session):
    """
        Waits until a session is estabilished
    """
    while not xmpp_client.is_in_session() == should_be_in_session:
        time.sleep(0.1)
    eq_(xmpp_client.is_in_session(), should_be_in_session)
