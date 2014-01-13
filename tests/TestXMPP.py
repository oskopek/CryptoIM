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
from nose.tools import ok_, eq_, with_setup

def test_xmpp_connection():
    xmpp_cli = xmpp.XMPPClient("cryptoim@jabber.de", "crypto_test")
    xmpp_cli.connect_server(should_block=False)
    yield check_connect, xmpp_cli

def check_connect(xmpp_client):
    """
        Check for xmpp.xmpp_client.connectServer and disconnectServer
    """

    eq_(xmpp_client.is_connected(), True)

    xmpp_client.disconnect_server()
    eq_(xmpp_client.is_connected(), False)

    # Uncomment the following to enable a second check -- note, will require a ~10s timeout
    """
    xmpp_client.connect_server()
    eq_(xmpp_client.is_connected(), True)

    xmpp_client.disconnect_server()
    eq_(xmpp_client.is_connected(), False)
    """
