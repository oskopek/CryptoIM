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

def init_messengers():
    """
        Initializes the messengers and connects them
    """

    crypto_shell = CryptoShell('main.cfg')

    messenger = xmpp.XMPPMessenger('cryptoim@jabber.de', 'crypto_test', crypto_shell)
    messenger.connect_server(should_block=False)

    crypto_shell2 = CryptoShell('main.cfg')
    messenger2 = xmpp.XMPPMessenger('cryptoim2@jabber.de', 'crypto_test2', crypto_shell2)
    messenger2.connect_server(should_block=False)

    waitForConnection(messenger, True)
    waitForConnection(messenger2, True)
    return messenger, messenger2

def test_connect():

    messenger, messenger2 = init_messengers()
    eq_(messenger.is_connected(), True)
    eq_(messenger2.is_connected(), True)

    messenger.disconnect_server()
    waitForConnection(messenger, False)
    messenger2.disconnect_server()
    waitForConnection(messenger2, False)

def test_send_message():

    messenger, messenger2 = init_messengers()
    waitForConnection(messenger, True)
    waitForConnection(messenger2, True)
    waitForSession(messenger, True)
    waitForSession(messenger2, True)
    msg = 'Hello, CryptoIM check_send_message!'
    recipient = messenger2.client.boundjid.full
    messenger.send_message(recipient, msg)

    waitForNonEmptyList(messenger.client.sent_msg_list)

    messenger.disconnect_server()
    messenger2.disconnect_server()
    waitForConnection(messenger, False)
    waitForConnection(messenger2, False)

    # Assert that messenger sent the message (it is bound to be sent after disconnect if it waits)
    ok_(1 == len(messenger.client.sent_msg_list))
    eq_(len(messenger.client.sent_jid_list), len(messenger.client.sent_msg_list))
    eq_(msg, messenger.client.sent_msg_list[-1])
    eq_(recipient, messenger.client.sent_jid_list[-1])

def test_connect_fail():

    crypto_shell = CryptoShell('main.cfg')

    # Wrong host
    messenger = xmpp.XMPPMessenger('cryptoim@jabber2.de', 'crypto_test', crypto_shell)
    assertDisconnect(messenger)


    # Wrong pass
    messenger = xmpp.XMPPMessenger('cryptoim@jabber.de', 'wrong_pass', crypto_shell)
    assertDisconnect(messenger)

    # Wrong name
    messenger = xmpp.XMPPMessenger('cryptoim0@jabber.de', 'crypto_test', crypto_shell)
    assertDisconnect(messenger)

def assertDisconnect(messenger):

    messenger.connect_server(should_block=False, should_reattempt=False)

    waitForConnection(messenger, False)

    messenger.disconnect_server()
    waitForConnection(messenger, False)

def test_receive_message():

    messenger, messenger2 = init_messengers()

    # Assert connected
    waitForConnection(messenger, True)
    waitForConnection(messenger2, True)
    waitForSession(messenger, True)
    waitForSession(messenger2, True)

    # Send and receive message
    plaintext = 'Hello, CryptoIM check_receive_message!'
    messenger.client.send_message(mto = messenger2.client.boundjid.full, mbody = 'test', mtype = 'error') # Test for dropping non-chat messages
    ciphertext = messenger.send_message(messenger2.client.boundjid.full, plaintext)

    waitForNonEmptyList(messenger2.client.received_msg_list)

    # Disconnect
    messenger.disconnect_server()
    waitForConnection(messenger, False)
    messenger2.disconnect_server()
    waitForConnection(messenger2, False)

    # Assert that messenger2 got it (it is bound to be received after disconnect if it waits)
    print(('Received msg list: ', messenger2.client.received_msg_list))
    print(('Received jid list: ', messenger2.client.received_jid_list))

    ok_(1 == len(messenger2.client.received_msg_list))
    eq_(len(messenger2.client.received_jid_list), len(messenger2.client.received_msg_list))
    eq_(plaintext, messenger2.client.received_msg_list[-1])
    eq_(messenger.client.boundjid.full, messenger2.client.received_jid_list[-1])

# Test tools

def waitForNonEmptyList(lst, timeout=100):
    """
        Waits until the list is non-empty.
        Timeout is set to 100 (in tenths of a second).
    """

    counter = 0
    while len(lst) < 1:
        if counter > timeout: break
        time.sleep(0.1)
        counter += 1
    ok_(len(lst) > 0)

def waitForConnection(messenger, should_be_connected, timeout=100):
    """
        Waits until a connection is estabilished.
        Timeout is set to 100 (in tenths of a second).
    """

    counter = 0
    while not messenger.is_connected() == should_be_connected:
        if counter > timeout: break
        time.sleep(0.1)
        counter += 1
    eq_(messenger.is_connected(), should_be_connected)

def waitForSession(messenger, should_be_in_session, timeout=100):
    """
        Waits until a session is estabilished.
        Timeout is set to 100 (in tenths of a second).
    """

    counter = 0
    while not messenger.is_in_session() == should_be_in_session:
        if counter > timeout: break
        time.sleep(0.1)
        counter += 1
    eq_(messenger.is_in_session(), should_be_in_session)
