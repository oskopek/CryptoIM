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
from nose.tools import ok_, eq_, nottest
import time

def test_xmpp():
    xmpp_cli = xmpp.XMPPClient('cryptoim@jabber.de', 'crypto_test')
    xmpp_cli.connect_server(should_block=False)

    eq_(xmpp_cli.is_connected(), True)

    yield check_connect, xmpp_cli

    # TODO fix this reuse
    xmpp_cli = xmpp.XMPPClient('cryptoim@jabber.de', 'crypto_test')
    xmpp_cli.connect_server(should_block=False)

    eq_(xmpp_cli.is_connected(), True)

    yield check_send_message, xmpp_cli

    # TODO fix this reuse
    xmpp_cli = xmpp.XMPPClient('cryptoim@jabber.de', 'crypto_test')
    xmpp_cli.connect_server(should_block=False)

    eq_(xmpp_cli.is_connected(), True)

    yield check_receive_message, xmpp_cli

def check_connect(xmpp_client):
    """
        Check for xmpp.XMPPClient.connect_server and disconnect_server
    """

    waitForConnection(xmpp_client, True)

    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)

    # Uncomment the following to enable a second check -- note, will require a ~10s timeout
    """
    xmpp_client.connect_server(should_block=False)
    waitForConnection(xmpp_client, True)

    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)
    """

def check_send_message(xmpp_client):
    """
        Check for xmpp.XMPPClient.send_message
    """

    waitForConnection(xmpp_client, True)

    while not xmpp_client.is_in_session():
        time.sleep(0.1)

    # TODO Works, but check
    xmpp_client.send_message('cryptoim2@jabber.de', 'Hello, CryptoIM check_send_message!')

    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)



def test_not_connect():
    """
        Check for xmpp.XMPPClient.connect_server and disconnect_server
    """

    # Wrong host
    xmpp_client = xmpp.XMPPClient('cryptoim@jabber2.de', 'crypto_test')
    xmpp_client.connect_server(should_block=False, should_reattempt=False)

    waitForConnection(xmpp_client, False)

    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)


    # Wrong pass
    xmpp_client = xmpp.XMPPClient('cryptoim@jabber.de', 'wrong_pass')
    xmpp_client.connect_server(should_block=False, should_reattempt=False)

    waitForConnection(xmpp_client, False)

    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)

    # Wrong name
    xmpp_client = xmpp.XMPPClient('cryptoim0@jabber.de', 'crypto_test')
    xmpp_client.connect_server(should_block=False, should_reattempt=False)

    waitForConnection(xmpp_client, False)

    xmpp_client.disconnect_server()
    waitForConnection(xmpp_client, False)


def check_receive_message(xmpp_client):
    """
        Check for CryptoXMPP.message
    """

    # Assert connected
    xmpp_client2 = xmpp.XMPPClient('cryptoim2@jabber.de', 'crypto_test2')
    xmpp_client2.connect_server(should_block=False)
    waitForConnection(xmpp_client, True)
    waitForConnection(xmpp_client2, True)

    while not (xmpp_client.is_in_session() and xmpp_client2.is_in_session()):
        time.sleep(0.1)

    # Send and receive message
    xmpp_client.send_message(xmpp_client2.xmpp.jid, 'Hello, CryptoIM check_receive_message!')

    # TODO Assert that xmpp_client2 got it

    # Disconnect
    xmpp_client.disconnect_server();
    waitForConnection(xmpp_client, False)
    xmpp_client2.disconnect_server()
    waitForConnection(xmpp_client2, False)
    waitForConnection(xmpp_client, False)

def waitForConnection(xmpp_client, should_be_connected):
    while not xmpp_client.is_connected() == should_be_connected:
        time.sleep(0.1)
    eq_(xmpp_client.is_connected(), should_be_connected)

