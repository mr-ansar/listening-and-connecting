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
'''A mimimal async, network service.

Listen for inbound connections at a configured address. Established
clients are expected to send a Hello, wait for a Welcome and then close
the connection. Termination is by user intervention, i.e. control-c.
'''
import ansar.connect as ar
from hello_welcome import *

# The server object.
def listen_at_address(self, settings):
	server_name = settings.server_name

	# Establish the listen.
	ipp = ar.HostPort(settings.host, settings.port)
	ar.listen(self, ipp)

	# At this point can expect;
	# 1. Confirmation of listen,
	# 2. Rejection of listen,
	# 3. User intervention.
	m = self.select(ar.Listening, ar.NotListening, ar.Stop)
	if isinstance(m, ar.NotListening):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

	# At this point can expect;
	# 1. Inbound connections,
	# 2. Requests from existing clients,
	# 3. Loss of connections,
	# 4. User intervention.
	while True:
		m = self.select(ar.Accepted, Hello, ar.Closed, ar.Abandoned, ar.Stop)
		if isinstance(m, ar.Accepted):
			self.console(f'Accepted {m.accepted_ipp}')			# Acquired a client.
			continue
		elif isinstance(m, (ar.Closed, ar.Abandoned)):
			self.console(f'Closed/Abandoned {m.opened_ipp}')	# Lost a client.
			continue
		elif isinstance(m, ar.Stop):	# Control-c.
			return ar.Aborted()			# Terminate this process.

		# Must have been the initial greeting.
		hello = m

		# Provide the expected response.
		welcome = Welcome(your_name=hello.my_name, my_name=server_name)
		self.reply(welcome)

		self.console(f'At server - {welcome}')

ar.bind(listen_at_address)

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

if __name__ == '__main__':
	ar.create_object(listen_at_address, factory_settings=factory_settings)
