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
'''A mimimal async, network client.

The client for the server in listen-at-address.py.
'''
import ansar.connect as ar
from hello_welcome import *

# The client object.
def connect_to_address(self, settings):
	client_name = settings.client_name

	# Initiate the connection.
	ipp = ar.HostPort(settings.host, settings.port)		# Where to expect the service.
	ar.connect(self, ipp)

	# At this point can expect;
	# 1. Confirmation of connection,
	# 2. Failure to connect,
	# 3. User intervention.
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.NotConnected):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()
	server_address = self.return_address	# Where the Connected message came from.

	# Make the request.
	hello = Hello(my_name=client_name)
	self.send(hello, server_address)

	# Expect a response. Which might be;
	# 1. Server acknowledgement,
	# 2. Loss of connection,
	# 3. User intervention.
	# 4. Time out.
	m = self.select(Welcome, ar.Closed, ar.Abandoned, ar.Stop, seconds=3.0)

	if isinstance(m, Welcome):		# Intended outcome.
		pass
	elif isinstance(m, (ar.Closed, ar.Abandoned)):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()
	elif isinstance(m, ar.SelectTimer):
		return ar.TimedOut(m)

	# Must have been the proper response.
	welcome = m

	self.console(f'At client - {welcome}')

	return welcome		# Return the result of Hello.

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

# Initial values.
factory_settings = Settings(client_name='Gladys', host='127.0.0.1', port=32011)

if __name__ == '__main__':
	ar.create_object(connect_to_address, factory_settings=factory_settings)
