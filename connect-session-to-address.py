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
'''A session-based async, network client.

A session-based implementation of the Enquiry-Ack sessions. A plug-in
replacement for connect-to-address or connect-fsm-to-address.
'''
import ansar.connect as ar
from hello_welcome import *

# Session object.
def connected_to_address(self, client_name, remote_address=None, **kv):
	hello = Hello(my_name=client_name)
	self.send(hello, remote_address)

	m = self.select(Welcome, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()
	return m

ar.bind(connected_to_address)

# Client object.
def connect_to_address(self, settings):
	client_name = settings.client_name

	ipp = ar.HostPort(settings.host, settings.port)				# Where to expect the service.
	session = ar.CreateFrame(connected_to_address, client_name)	# Description of a session.
	ar.connect(self, ipp, session=session)
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.NotConnected):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

	# Session has started.
	m = self.select(ar.Abandoned, ar.Closed, ar.Stop)
	if isinstance(m, ar.Abandoned):
		return m
	elif isinstance(m, ar.Closed):
		return m.value
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

ar.bind(connect_to_address)

#
#
class Settings(object):
	def __init__(self, client_name=None, host=None, port=None):
		self.client_name = client_name
		self.host = host
		self.port = port

SETTINGS_SCHEMA = {
	'client_name': str,
	'host': str,
	'port': int,
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

factory_settings = Settings(client_name='Gladys', host='127.0.0.1', port=32011)

if __name__ == '__main__':
	ar.create_object(connect_to_address, factory_settings=factory_settings)
