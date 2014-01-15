#!/usr/bin/env python
# encoding: utf-8

"""
   Copyright 2014 CryptoIM Development Team

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this logfile except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import cmd

import cryptoim.xmpp

class CryptoShell(cmd.Cmd):
    intro = 'Welcome to CryptoIM!   Type help or ? to list commands.\n'
    prompt = '(cryptoim) '
    xmpp_client = None


    # -- basic commands --
    def do_exit(self, arg):
        'Quit CryptoIM'

        self.do_disconnect(arg)
        print('Thank you for using CryptoIM!')
        quit()


    # -- overrides --
    def emptyline(self):
        return


    # -- xmpp commands --
    def do_connect(self, arg):
        'connect JID PASSWORD'

        if self.xmpp_client and self.xmpp_client.is_connected():
            self.print_cmd('Already connected!')
            return

        splitted = arg.split(' ')
        self.xmpp_client = cryptoim.xmpp.XMPPClient(splitted[0], splitted[1], self)
        self.xmpp_client.connect_server()

    def do_disconnect(self, arg):
        'disconnect'
        if not self.xmpp_client or not self.xmpp_client.is_connected():
            self.print_cmd('Already disconnected!')
            return

        self.xmpp_client.disconnect_server()

    def do_send(self, arg):
        'send toJID msg'
        if not self.xmpp_client or not self.xmpp_client.is_in_session():
            self.print_cmd('Connect first!')
            return

        splitted = arg.split(' ')
        self.xmpp_client.send_message(splitted[0], splitted[1])

        # TODO fix the jid part
        self.print_msg(self.xmpp_client.xmpp.jid, splitted[1])


    # -- tools --

    def print_cmd(self, string):
        print(string)

    def print_msg(self, jid, msg):
        # TODO interface with cmd in a normal way
        self.print_cmd(jid + ': ' + msg)

    def print_debug(self, msg):
        #self.print_cmd('DEBUG: ' + msg)
        return
