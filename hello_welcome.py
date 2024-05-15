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
'''Message definitions for listen-at-address, connect-to-address and others.

'''
import ansar.encode as ar

__all__ = [
	'Hello',
	'Welcome',
]

class Hello(object):
	def __init__(self, my_name=None):
		self.my_name = my_name

class Welcome(object):
	def __init__(self, your_name=None, my_name=None):
		self.your_name = your_name
		self.my_name = my_name
	
	def __str__(self):
		return f'Hello "{self.your_name}", my name is "{self.my_name}"'

SCHEMA = {
	'my_name': str,
	'your_name': str,
}

ar.bind(Hello, object_schema=SCHEMA)
ar.bind(Welcome, object_schema=SCHEMA)
