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

class CryptoShell(cmd.Cmd):
    intro = 'Welcome to CryptoIM!   Type help or ? to list commands.\n'
    prompt = '(cryptoim) '

    # ----- basic commands -----
    def do_exit(self, arg):
        'Quit CryptoIM'

        print('Thank you for using CryptoIM!')
        quit()


    # -- overrides --
    def emptyline(self):
        return


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))
