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

Original LICENSE:

    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file NOTICE.rst file for copying permission.
"""

import logging, sleekxmpp

import cryptoim.encryptor_core as encryptor
import cryptoim.decryptor_core as decryptor
import cryptoim.key_exchange as keyex

class CryptoXMPP(sleekxmpp.ClientXMPP):
    """
        A SleekXMPP client (inherits from ClientXMPP),
        provides handling of incoming and outgoing messages
        with a built-in Diffie-Hellman key exchange.
    """

    def __init__(self, jid, password, shell):
        """
            Initializes the object with given parameters,
            initializes empty fields
            and sets up anything related to the xmpp client.
        """

        # Strip the resource, let the server generate one
        jid = strip_resource(jid)

        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler('session_start', self.on_session_start)
        self.add_event_handler('session_end', self.on_session_end)
        self.add_event_handler('message', self.on_message)
        self.add_event_handler('connected', self.on_connected)
        self.add_event_handler('disconnected', self.on_disconnected)

        # Accept and create bidirectional subscription requests:
        self.auto_authorize = True
        self.auto_subscribe = True

        # Initialize fields
        self.shell = shell
        self.is_in_session = False
        self.is_connected = False

        # Make sure to only store bare JIDs here!
        self.msg_queue = dict()
        # Store full JIDs here
        self.key_queue = dict()

        # Logging
        self.received_msg_list = []
        self.received_jid_list = []
        self.sent_msg_list = []
        self.sent_jid_list = []

        # Setup the ClientXMPP and register plugins. Note that while plugins may
        # have interdependencies, the order in which you register them does
        # not matter.
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping

    def on_connected(self, event):
        """
            Process the connected event.
        """

        self.is_connected = True
        self.shell.print_debug('Connection started.')

    def on_disconnected(self, event):
        """
            Process the disconnected event.
        """

        self.is_connected = False
        self.shell.print_debug('Connection ended.')

    def on_session_end(self, event):
        """
            Process the session_end event.
        """

        self.is_in_session = False
        self.shell.print_cmd('Disconnected!')
        self.shell.print_debug('Session ended.')

    def on_session_start(self, event):
        """
            Process the session_start event.
        """

        self.send_presence(ppriority=120)
        self.get_roster()
        self.is_in_session = True
        self.shell.print_cmd('Connected!')
        self.shell.print_debug('Session started.')

    def on_message(self, msg):
        """
            Process incoming message stanzas.
        """

        if msg['type'] not in ('chat', 'normal'):
            return # Ignore nonchat messages

        sender = msg['from']
        text = msg['body']

        # DH key exchange: https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Explanation_including_encryption_mathematics

        if text.startswith('SYN;'): # receiving
            prime, base, a_public = keyex.decode_syn(msg['body'])
            b = keyex.generate_random(2, 100)
            b_public = keyex.make_public_key(prime, base, b)
            key = str(keyex.make_final_key(prime, a_public, b))

            self.send_message(mto = sender.full, mbody = keyex.encode_ack(b_public), mtype = 'chat')
            self.key_queue[sender.full] = key

        elif text.startswith('ACK;'): # sending
            q_entry = self.msg_queue[sender.bare]
            msg_text = q_entry[0]
            prime = q_entry[1]
            a = q_entry[2]
            b_public = keyex.decode_ack(msg['body'])
            key = str(keyex.make_final_key(prime, b_public, a))
            ciphertext = encryptor.encrypt(msg_text, key)
            self.send_message(mto = sender.full, mbody = ciphertext, mtype = 'chat')

            del self.msg_queue[sender.bare] # q_entry

            # Log:
            self.sent_jid_list.append(sender.full)
            self.sent_msg_list.append(msg_text)

        else:
            ciphertext = text
            key = self.key_queue[sender.full]
            decrypted_message = decryptor.decrypt(ciphertext, key)
            self.shell.print_msg(sender.bare, decrypted_message)

            del self.key_queue[sender.full] # key

            # Log:
            self.received_jid_list.append(sender.full)
            self.received_msg_list.append(decrypted_message)

class XMPPMessenger(object):
    """
        A simple high-level wrapper for CryptoXMPP
    """

    LOG_LEVEL = logging.CRITICAL

    def __init__(self, jid, password, shell, loglevel=LOG_LEVEL):
        """
            Initializes the client and logging
        """

        # Setup logging.
        logging.basicConfig(level=loglevel,
                            format='%(levelname)-8s %(message)s')

        # Setup the actual client
        self.client = CryptoXMPP(jid, password, shell)

    def connect_server(self, should_block=False, should_reattempt=True):
        """
            Connects the client to the server,
            specifying thread blocking and reattempting on failed connection.
        """

        if self.client.connect(reattempt=should_reattempt):
            # If you do not have the dnspython library installed, you will need
            # to manually specify the name of the server if it does not match
            # the one in the JID. For example, to use Google Talk you would
            # need to use:
            #
            # if client.connect(('talk.google.com', 5222)):
            #     ...
            self.client.process(block=should_block)

    def disconnect_server(self):
        """
            Disconnects the client from the server.
        """

        self.client.disconnect(wait=True)

    def is_connected(self):
        """
            Checks if the client is currently connected to the server.
        """

        return self.client.is_connected

    def is_in_session(self):
        """
            Checks if the client is currently in a session
        """

        return self.client.is_in_session

    def send_message(self, recipient, msg):
        """
            Sends a chat message to the designated recipient.

            Actually only queues the message into a msg_queue, sending is a property of the client.
        """

        prime = keyex.prime_pick()
        base = keyex.base_pick()
        a = keyex.generate_random(2, 100)
        a_public = keyex.make_public_key(prime, base, a)
        syn_msg = keyex.encode_syn(prime, base, a_public)

        self.client.send_message(mto = recipient, mbody = syn_msg, mtype = 'chat')
        self.client.msg_queue[strip_resource(recipient)] = (msg, prime, a) # Do not store resource in the msg_queue

# Tool functions:

def strip_resource(jid):
    """
        Strips all the characters after a forward-slash '/', inclusive
    """

    if '/' in jid:
        jid = jid[:jid.index('/')]
    return jid
