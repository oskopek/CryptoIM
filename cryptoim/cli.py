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

import cmd, sys, copy

import cryptoim.xmpp

if sys.version_info < (3, 0):
    import ConfigParser as configparser
else:
    import configparser as configparser


class CryptoShell(cmd.Cmd):
    intro = 'Welcome to CryptoIM!   Type help or ? to list commands.\n'
    prompt = '(cryptoim) '
    xmpp_client = None
    config = None


    def __init__(self, configfile):
        # super().__init__() # Python 3 only
        cmd.Cmd.__init__(self)
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

    # -- basic commands --
    def do_exit(self, arg):
        'Quit CryptoIM'

        self.do_disconnect(arg)
        self.print_cmd('Thank you for using CryptoIM!')
        quit()

    def do_q(self, arg):
        self.do_exit(arg)


    # -- overrides --
    def emptyline(self):
        return

    # -- xmpp commands --
    def do_connect(self, arg):
        'connect JID PASSWORD or connect CONNECTION_NAME'
        splitted = arg.split(' ')
        if not arg or (not len(splitted) == 1 and not len(splitted) == 2):
            self.print_cmd('Invalid number of arguments!')
            return

        if self.xmpp_client and self.xmpp_client.is_connected():
            self.print_cmd('Already connected!')
            return

        conn_jid = None
        conn_pass = None

        if len(splitted) == 1:
            if splitted[0] in self.config.sections():
                username = self.config.get(arg, 'Username') # self.config[arg]['Username']
                host = self.config.get(arg, 'Host') # self.config[arg]['Host']
                conn_jid = username + '@' + host
                conn_pass = self.config.get(arg, 'Password') # self.config[arg]['Password']
            else:
                self.print_cmd('Connection ' + splitted[0] + ' doesn\'t exist');

        elif len(splitted) == 2:
            conn_jid = splitted[0]
            conn_pass = splitted[1]

        conn_jid += '/cryptoim' # Adds a static resource
        self.xmpp_client = cryptoim.xmpp.XMPPClient(conn_jid, conn_pass, self)
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
        self.print_cmd(self.address_format(self.xmpp_client.xmpp.jid, splitted[1]))


    # -- tools --

    def print_cmd(self, string):
        self.stdout.write(string + '\n')
        self.stdout.flush()

    def address_format(self, jid, msg):
        return jid + ': ' + msg

    def print_msg(self, jid, msg):
        # TODO interface with cmd in a normal way
        backup = copy.copy(self.prompt)
        self.stdout.write('\r                                                                                                                                                        \r')
        self.stdout.flush()
        self.print_cmd(self.address_format(jid, msg))
        self.stdout.write(backup)
        self.stdout.flush()

    def print_debug(self, msg):
        #self.print_cmd('DEBUG: ' + msg)
        pass
