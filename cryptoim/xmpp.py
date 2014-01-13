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

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file NOTICE.rst file for copying permission.
"""

import logging
import sleekxmpp

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
"""
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input
"""

class CryptoXMPP(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP client.
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

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
        self.send_presence()
        self.get_roster()

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
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()
        print("DEBUG: MSG: %(body)s" % msg)


class XMPPClient(object):
    """
        The XMPP client object, used as a wrapper for the SleekXMPP client.
    """

    def __init__(self, jid, password, loglevel=logging.DEBUG):
        """
            Initializes the ClientXMPP, logging, etc
        """

        # Setup logging.
        logging.basicConfig(level=loglevel,
                            format='%(levelname)-8s %(message)s')

        # Setup the ClientXMPP and register plugins. Note that while plugins may
        # have interdependencies, the order in which you register them does
        # not matter.
        self.xmpp = CryptoXMPP(jid, password)
        self.xmpp.register_plugin('xep_0030') # Service Discovery
        self.xmpp.register_plugin('xep_0004') # Data Forms
        self.xmpp.register_plugin('xep_0060') # PubSub
        self.xmpp.register_plugin('xep_0199') # XMPP Ping


    def connect_server(self, should_block=False):
        """
            Connects the ClientXMPP to the server, specify thread blocking.
        """

        # Connect to the XMPP server and start processing XMPP stanzas.
        if self.xmpp.connect():
            # If you do not have the dnspython library installed, you will need
            # to manually specify the name of the server if it does not match
            # the one in the JID. For example, to use Google Talk you would
            # need to use:
            #
            # if xmpp.connect(('talk.google.com', 5222)):
            #     ...
            self.xmpp.process(block=should_block)
            print("Connected.")
        else:
            print("Unable to connect.")

    def disconnect_server(self):
        """
            Disconnects the ClientXMPP from the server.
        """

        self.xmpp.disconnect(wait=True)

    def is_connected(self):
        """
            Checks if the ClientXMPP is currently connected to the server.
        """

        return self.xmpp.state.current_state() == "connected"
