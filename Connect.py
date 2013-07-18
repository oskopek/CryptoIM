import cmd, sys, string, os
import logging
import getpass
from optparse import OptionParser

import sleekxmpp

from XMPPClient import XMPPClient

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
	from sleekxmpp.util.misc_ops import setdefaultencoding
	setdefaultencoding('utf8')
else:
	raw_input = input

class Connect(cmd.Cmd):

	global xmpp

	def __init__(self, args):
		cmd.Cmd.__init__(self)
		self.prompt = "> "

		# Setup the command line arguments.
		optp = OptionParser()

		# Output verbosity options.
		optp.add_option('-q', '--quiet', help='set logging to ERROR',
					action='store_const', dest='loglevel',
					const=logging.ERROR, default=logging.INFO)
		optp.add_option('-d', '--debug', help='set logging to DEBUG',
					action='store_const', dest='loglevel',
					const=logging.DEBUG, default=logging.INFO)
		optp.add_option('-v', '--verbose', help='set logging to COMM',
					action='store_const', dest='loglevel',
					const=5, default=logging.INFO)

		# JID and password options.
		optp.add_option("-j", "--jid", dest="jid",
					help="JID to use")
		optp.add_option("-p", "--password", dest="password",
					help="password to use")

		opts, args = optp.parse_args()

		# Setup logging.
		logging.basicConfig(level=opts.loglevel,
						format='%(levelname)-8s %(message)s')

		if opts.jid is None:
			opts.jid = raw_input("Username: ")
		if opts.password is None:
			opts.password = getpass.getpass("Password: ")

		# Setup the XMPPClient and register plugins. Note that while plugins may
		# have interdependencies, the order in which you register them does
		# not matter.
		global xmpp
		xmpp = XMPPClient(opts.jid, opts.password, self)
		xmpp.register_plugin('xep_0030') # Service Discovery
		xmpp.register_plugin('xep_0004') # Data Forms
		xmpp.register_plugin('xep_0060') # PubSub
		xmpp.register_plugin('xep_0199') # XMPP Ping


		# Connect to the XMPP server and start processing XMPP stanzas.
		if xmpp.connect():
		# If you do not have the dnspython library installed, you will need
		# to manually specify the name of the server if it does not match
		# the one in the JID. For example, to use Google Talk you would
		# need to use:
		#
		# if xmpp.connect(('talk.google.com', 5222)):
		#     ...
			xmpp.process(block=False)
			print("Done")
		else:
			print("Unable to connect.")


	## Command definitions ##
	def do_history(self, args):
		"""Print a list of commands that have been entered"""
		print self._hist

	def do_disconnect(self, args):
		"""
		Disconnect from server
		"""
		global xmpp
		xmpp.quit_disconnect()
		return -1

	def do_message(self, args):
		"""Send a message to a client - use full jabber id"""
		client = raw_input("Client: ")
		message = raw_input("Message: ")
		global xmpp
		xmpp.sendmessage(client, message)

	def do_buddylist(self, args):
		"""Get the buddy list"""
		global xmpp
		print xmpp.getbuddylist()

	def message(self, msg):
		print msg['from'], msg['body']

	def do_help(self, args):
		"""Get help on commands
		'help' or '?' with no arguments prints a list of commands for which help is available
		'help <command>' or '? <command>' gives help on <command>
		"""
		## The only reason to define this method is for the help text in the doc string
		cmd.Cmd.do_help(self, args)

	## Override methods in Cmd object ##
	def preloop(self):
		"""Initialization before prompting user for commands.
		Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
		"""
		cmd.Cmd.preloop(self)   ## sets up command completion
		self._hist    = []      ## No history yet
		self._locals  = {}      ## Initialize execution namespace for user
		self._globals = {}

	def postloop(self):
		"""Take care of any unfinished business.
		Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
		"""
		cmd.Cmd.postloop(self)   ## Clean up command completion
		print "Exiting..."

	def precmd(self, line):
		""" This method is called after the line has been input but before
			it has been interpreted. If you want to modifdy the input line
			before execution (for example, variable substitution) do it here.
		"""
		self._hist += [ line.strip() ]
		return line

	def postcmd(self, stop, line):
		"""If you want to stop the console, return something that evaluates to true.
		If you want to do some post command processing, do it here.
		"""
		return stop

	def emptyline(self):
		"""Do nothing on empty input line"""
		pass

	def default(self, line):
		"""Called on an input line when the command prefix is not recognized.
		In that case we execute the line as Python code.
		"""
		pass
