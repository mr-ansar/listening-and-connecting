# Author: Scott Woods <scott.18.ansar@gmail.com>
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
'''A mimimal FSM, network client.

A finite-state-machine implementation of the Enquiry-Ack sessions. A plug-in
replacement for connect-to-address or connect-session-to-address.
'''
import ansar.connect as ar
from hello_welcome import *

# Client FSM object.
class INITIAL: pass
class PENDING: pass
class CONNECTED: pass

class ConnectToAddress(ar.Point, ar.StateMachine):
	def __init__(self, settings):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.settings = settings
		self.client_name = settings.client_name
		self.ipp = None
		self.connected = None

def ConnectToAddress_INITIAL_Start(self, message):
	self.ipp = ar.HostPort(self.settings.host, self.settings.port)
	ar.connect(self, self.ipp)
	return PENDING

def ConnectToAddress_PENDING_Connected(self, message):
	self.connected = message
	hello = Hello(my_name=self.client_name)
	self.reply(hello)
	return CONNECTED

def ConnectToAddress_PENDING_NotConnected(self, message):
	self.complete(message)

def ConnectToAddress_PENDING_Stop(self, message):
	self.complete(ar.Aborted())

def ConnectToAddress_CONNECTED_Welcome(self, message):
	self.complete(message)

def ConnectToAddress_CONNECTED_Abandoned(self, message):
	self.complete(message)

def ConnectToAddress_CONNECTED_Stop(self, message):
	self.complete(ar.Aborted())

CONNECT_TO_ADDRESS_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	PENDING: (
		(ar.Connected, ar.NotConnected, ar.Stop), ()
	),
	CONNECTED: (
		(Welcome, ar.Abandoned, ar.Stop,), ()
	),
}

ar.bind(ConnectToAddress, CONNECT_TO_ADDRESS_DISPATCH)

#
#
class Settings(object):
	def __init__(self, client_name=None, host=None, port=None):
		self.client_name = client_name
		self.host = host
		self.port = port

SETTINGS_SCHEMA = {
	'client_name': ar.Unicode(),
	'host': ar.Unicode(),
	'port': ar.Integer8(),
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

factory_settings = Settings(client_name='Gladys', host='127.0.0.1', port=32011)

if __name__ == '__main__':
	ar.create_object(ConnectToAddress, factory_settings=factory_settings)
