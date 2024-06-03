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
'''A session-based async, network service.

A session-based implementation of the Enquiry-Ack sessions. A plug-in
replacement for listen-at-address or listen-fsm-at-address.
'''
import ansar.connect as ar
from hello_welcome import *

# Session object.
def accepted_at_address(self, server_name, **kv):
	while True:
		m = self.select(Hello, ar.Stop)
		if isinstance(m, Hello):
			welcome = Welcome(your_name=m.my_name, my_name=server_name)
			self.reply(welcome)
		elif isinstance(m, ar.Stop):
			return ar.Aborted()

ar.bind(accepted_at_address)

# Server object.
def listen_at_address(self, settings):
	server_name = settings.server_name

	# Establish the listen.
	ipp = ar.HostPort(settings.host, settings.port)
	session = ar.CreateFrame(accepted_at_address, server_name)
	ar.listen(self, ipp, session=session)
	m = self.select(ar.Listening, ar.NotListening, ar.Stop)
	if isinstance(m, ar.NotListening):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

	# Ready for inbound connections.
	while True:
		m = self.select(ar.Accepted, ar.Abandoned, ar.Stop)
		if isinstance(m, ar.Accepted):
			self.console(f'Accepted at {m.accepted_ipp}')
			continue
		elif isinstance(m, ar.Abandoned):
			self.console(f'Abandoned')
			continue
		elif isinstance(m, ar.Stop):	# Control-c.
			return ar.Aborted()

ar.bind(listen_at_address)

# Configuration for this executable.
class Settings(object):
	def __init__(self, server_name=None, host=None, port=None):
		self.server_name = server_name
		self.host = host
		self.port = port

SETTINGS_SCHEMA = {
	'server_name': str,
	'host': str,
	'port': int,
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(server_name='Buster', host='127.0.0.1', port=32011)

# Entry point.
if __name__ == '__main__':
	ar.create_object(listen_at_address, factory_settings=factory_settings)
