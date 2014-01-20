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

import cmd, sys, copy

import cryptoim.xmpp

if sys.version_info < (3, 0):
    import ConfigParser as configparser
else:
    import configparser as configparser


class CryptoShell(cmd.Cmd):
    """
        CryptoShell
    """

    intro = 'Welcome to CryptoIM!   Type help or ? to list commands.\n'
    prompt = '(cryptoim) '
    xmpp_client = None
    config = None
    config_file = None
    current_chat = None


    def __init__(self, config_file):
        """
            CryptoShell init
        """

        # super().__init__() # Python 3 only
        cmd.Cmd.__init__(self)
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.config_file = config_file

    # -- basic commands --
    def do_exit(self, arg):
        'Quit CryptoIM'

        self.do_disconnect(arg)
        self.print_cmd('Thank you for using CryptoIM!')
        quit()

    def do_q(self, arg):
        'Alias for quit'
        self.do_exit(arg)


    # -- overrides --
    def emptyline(self):
        pass

    # -- xmpp commands --
    def do_connect(self, arg):
        'connect JID PASSWORD or connect CONNECTION_NAME'
        splitted = arg.split(' ')
        if not arg or (not len(splitted) == 1 and not len(splitted) == 2):
            self.print_cmd('Invalid number of arguments!')
            return False

        if self.xmpp_client and self.xmpp_client.is_connected():
            self.print_cmd('Already connected!')
            return False

        conn_jid = None
        conn_pass = None

        if len(splitted) == 1:
            if splitted[0] in self.config.sections():
                username = self.config.get(arg, 'Username') # self.config[arg]['Username']
                host = self.config.get(arg, 'Host') # self.config[arg]['Host']
                conn_jid = username + '@' + host
                conn_pass = self.config.get(arg, 'Password') # self.config[arg]['Password']
            else:
                self.print_cmd('Connection ' + splitted[0] + ' doesn\'t exist')
                return False

        elif len(splitted) == 2:
            conn_jid = splitted[0]
            conn_pass = splitted[1]

        conn_jid += '/cryptoim' # Adds a static resource
        self.xmpp_client = cryptoim.xmpp.XMPPClient(conn_jid, conn_pass, self)
        self.xmpp_client.connect_server()
        return True


    def do_disconnect(self, arg):
        'disconnect'
        if not self.xmpp_client or not self.xmpp_client.is_connected():
            self.print_cmd('Already disconnected!')
            return False

        self.xmpp_client.disconnect_server()
        return True

    def do_s(self, arg):
        'send toJID msg'
        return(self.do_send(arg))

    def do_send(self, arg):
        'send toJID msg'
        if not self.xmpp_client or not self.xmpp_client.is_in_session():
            self.print_cmd('Connect first!')
            return False

        splitted = arg.split(' ')

        if self.current_chat != None:
            recipient = self.current_chat
            message = ' '.join(splitted)

        else:
            recipient = splitted[0]
            message = ' '.join(splitted[1:])

        self.xmpp_client.send_message(recipient, message)
        self.print_cmd(address_format(self.xmpp_client.xmpp.jid, message))
        return True

    def do_addfriend(self, arg):
        'addfriend name jid'
        splitted = arg.split(' ')

        if splitted[0] in self.config['friends']:
            self.print_cmd('Already in your friend list.')
            return False

        self.config.set('friends', splitted[0], splitted[1])
        with open(self.config_file, 'w') as conf:
            self.config.write(conf)
        return True

    def do_removefriend(self, arg):
        'removefriend name'
        splitted = arg.split(' ')

        if splitted[0] not in self.config['friends']:
            self.print_cmd('Not in your friend list.')
            return False

        self.config.remove_option('friends', splitted[0])
        with open(self.config_file, 'w') as conf:
            self.config.write(conf)
        return True

    def do_chat(self, arg):
        """
            chat JID
        """
        if not arg:
            return False
        else:
            self.print_cmd('Opening chat window with: ' + arg.split(' ')[0])
            self.current_chat = arg.split(' ')[0]
            self.prompt = '(' + self.current_chat.split('@')[0] + ') '
        return True

    def do_stopchat(self, arg):
        """
            stopchat
        """
        self.prompt = '(cryptoim) '
        self.current_chat = None
        self.print_cmd('Closing chat window.')
        return True

    # -- tools --

    def print_cmd(self, string):
        """
            Prints a string to the console
        """
        self.stdout.write(string + '\n')
        self.stdout.flush()

    def print_msg(self, jid, msg):
        """
            Prints a message (jid + msg), correctly formatted using address_format
            without erasing typed content. TODO implement the erasing and backup
        """

        backup = copy.copy(self.prompt)
        self.stdout.write('\r')
        self.stdout.flush()
        self.print_cmd(address_format(jid, msg))
        self.stdout.write(backup)
        self.stdout.flush()

    def print_debug(self, msg):
        """
            Prints debug messages
        """
        #self.print_cmd('DEBUG: ' + msg)
        pass

# End of class

def address_format(jid, msg):
    """
        Formats a jid and message to correctly display in the log
    """
    return(jid + ': ' + msg)
