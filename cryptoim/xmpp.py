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
        A simple SleekXMPP client.
    """

    def __init__(self, jid, password, parent):
        # Strip the resource, let the server generate one
        jid = strip_resource(jid)

        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('session_end', self.session_end)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler('message', self.message)

        self.add_event_handler('connected', self.connected)
        self.add_event_handler('disconnected', self.disconnected)

        # Accept and create bidirectional subscription requests:
        self.auto_authorize = True
        self.auto_subscribe = True

        self.parent = parent
        self.in_session = False
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

    def connected(self, event):
        """
            Process the connected event.
        """

        self.is_connected = True
        self.parent.print_debug('Connection started.')

    def disconnected(self, event):
        """
            Process the disconnected event.
        """

        self.is_connected = False
        self.parent.print_debug('Connection ended.')

    def session_end(self, event):
        """
            Process the session_end event.
        """

        self.in_session = False
        self.parent.print_debug('Session ended.')

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence(ppriority=120)
        self.get_roster()
        self.in_session = True
        self.parent.print_cmd('Connected!')
        self.parent.print_debug('Session started.')

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """

        if msg['type'] not in ('chat', 'normal'):
            return # Ignore nonchat messages

        sender = msg['from']
        text = msg['body']

        # DH key exchange: https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Explanation_including_encryption_mathematics

        if text.startswith('SYN;'): # receiving
            prime, base, A = keyex.decode_syn(msg['body'])
            b = keyex.generate_random(2, 100)
            B = keyex.make_public_key(prime, base, b)
            key = str(keyex.make_final_key(prime, A, b))

            self.send_message(mto = sender.full, mbody = keyex.encode_ack(B), mtype = 'chat')
            self.key_queue[sender.full] = key



        elif text.startswith('ACK;'): # sending
            q_entry = self.msg_queue[sender.bare]
            msg_text = q_entry[0]
            prime = q_entry[1]
            a = q_entry[2]
            B = keyex.decode_ack(msg['body'])
            key = str(keyex.make_final_key(prime, B, a))
            ciphertext = encryptor.encrypt(msg_text, key)
            self.send_message(mto = sender.full, mbody = ciphertext, mtype = 'chat')

            del q_entry # TODO check if it actually gets removed

            # Log:
            self.sent_jid_list.append(sender.full)
            self.sent_msg_list.append(msg_text)

        else:
            ciphertext = text
            key = self.key_queue[sender.full]
            decrypted_message = decryptor.decrypt(ciphertext, key)
            self.parent.print_msg(sender.bare, decrypted_message)

            del key # TODO check if it actually gets removed

            # Log:
            self.received_jid_list.append(sender.full)
            self.received_msg_list.append(decrypted_message)


class XMPPClient(object):
    """
        Used as a simple wrapper for CryptoXMPP
    """
    LOG_LEVEL = logging.CRITICAL
    xmpp = None

    def __init__(self, jid, password, parent, loglevel=LOG_LEVEL):
        """
            Initializes the CryptoXMPP and logging
        """

        # Setup logging.
        logging.basicConfig(level=loglevel,
                            format='%(levelname)-8s %(message)s')

        # Setup the actual client
        self.xmpp = CryptoXMPP(jid, password, parent)

    def connect_server(self, should_block=False, should_reattempt=True):
        """
            Connects the CryptoXMPP to the server,
            specifying thread blocking and reattempting on failed connection.
        """

        if self.xmpp.connect(reattempt=should_reattempt):
            # TODO If you do not have the dnspython library installed, you will need
            # to manually specify the name of the server if it does not match
            # the one in the JID. For example, to use Google Talk you would
            # need to use:
            #
            # if xmpp.connect(('talk.google.com', 5222)):
            #     ...
            self.xmpp.process(block=should_block)

    def disconnect_server(self):
        """
            Disconnects the CryptoXMPP from the server.
        """

        self.xmpp.disconnect(wait=True)

    def is_connected(self):
        """
            Checks if the CryptoXMPP is currently connected to the server.
        """

        return self.xmpp.is_connected

    def is_in_session(self):
        """
            Checks if the CryptoXMPP is currently in a session
        """

        return self.xmpp.in_session

    def send_message(self, recipient, msg):
        """
            Sends a chat message to the designated recipient.
        """

        prime = keyex.prime_pick()
        base = keyex.base_pick()
        a = keyex.generate_random(2, 100)
        A = keyex.make_public_key(prime, base, a)

        self.xmpp.send_message(mto = recipient, mbody = keyex.encode_syn(prime, base, A), mtype = 'chat')
        self.xmpp.msg_queue[strip_resource(recipient)] = (msg, prime, a) # Do not store resource in msg_queue

# Tool functions:

def strip_resource(jid):
    """
        Strips all the characters after a forward-slash '/', inclusive
    """

    if '/' in jid:
        jid = jid[:jid.index('/')]
    return jid
