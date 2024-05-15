# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2024 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''A mimimal FSM, network service.

A finite-state-machine implementation of the Enquiry-Ack sessions. A plug-in
replacement for listen-at-address or listen-session-at-address.
'''
import ansar.connect as ar
from hello_welcome import *


# Server FSM object.
class INITIAL: pass
class PENDING: pass
class LISTENING: pass

class ListenAtAddress(ar.Point, ar.StateMachine):
	def __init__(self, settings):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.settings = settings
		self.server_name = settings.server_name
		self.ipp = None
		self.listening = None

def ListenAtAddress_INITIAL_Start(self, message):
	self.ipp = ar.HostPort(self.settings.host, self.settings.port)
	ar.listen(self, self.ipp)
	return PENDING

def ListenAtAddress_PENDING_Listening(self, message):
	self.listening = message
	return LISTENING

def ListenAtAddress_PENDING_NotListening(self, message):
	self.complete(message)

def ListenAtAddress_PENDING_Stop(self, message):
	self.complete(ar.Aborted())

def ListenAtAddress_LISTENING_Accepted(self, message):
	self.console(f'Accepted at {message.accepted_ipp}')
	return LISTENING

def ListenAtAddress_LISTENING_Hello(self, message):
	welcome = Welcome(your_name=message.my_name, my_name=self.server_name)
	self.reply(welcome)
	return LISTENING

def ListenAtAddress_LISTENING_Abandoned(self, message):
	self.console(f'Abandoned')
	return LISTENING

def ListenAtAddress_LISTENING_Stop(self, message):
	self.complete(ar.Aborted())

LISTEN_AT_ADDRESS_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	PENDING: (
		(ar.Listening, ar.NotListening, ar.Stop), ()
	),
	LISTENING: (
		(ar.Accepted, Hello, ar.Abandoned, ar.Stop,), ()
	),
}

ar.bind(ListenAtAddress, LISTEN_AT_ADDRESS_DISPATCH)

# Configuration for this executable.
class Settings(object):
	def __init__(self, server_name=None, host=None, port=None):
		self.server_name = server_name
		self.host = host
		self.port = port

SETTINGS_SCHEMA = {
	'server_name': ar.Unicode(),
	'host': ar.Unicode(),
	'port': ar.Integer8(),
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(server_name='Buster', host='127.0.0.1', port=32011)

# Entry point.
if __name__ == '__main__':
	ar.create_object(ListenAtAddress, factory_settings=factory_settings)
