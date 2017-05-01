#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import six
import string

printable = set(string.printable)

def isprint(x):
    return set(x) < printable

try:
    import xmlrpc.client as xmlrpclib
    from xmlrpc.server import SimpleXMLRPCServer
except:
    import xmlrpclib
    from SimpleXMLRPCServer import SimpleXMLRPCServer

# Disable use of the accelerated Unmarshaller, so that we
# can add our own types.
xmlrpclib.FastUnmarshaller = None

# Declare code to marshal / unmarshal the only two types we really
# care about: Integers and Binary data.  The built-in marshallers
# are quite inferior.
def marshall_int(self, value, write):
    template = "<value><i8>%d</i8></value>"
    value = int(value)
    write(template % value)

def marshall_binary(self, value, write):
    template = "<value><binary>%s,%s</binary></value>"

    encoding = None

    # Python2 string and bytes are the same
    if isinstance(value, bytes):
        encoding = 'bytes'

    # Python2 unicode and Python3 string need to be *encoded* to bytes
    elif isinstance(value, six.string_types):
        try:
            value.encode('latin-1')
            encoding = 'latin-1'
        except Exception as e:
            print(type(e), e)
            pass

        try:
            value.encode('utf-8')
            encoding = 'utf-8'
        except Exception as e:
            print(type(e), e)
            pass

        value = value.encode(encoding)

    elif isinstance(value, bytearray):
        encoding = 'bytearray'

    value = codecs.encode(value, 'hex')
    value = value.decode('latin-1')

    print(template % (encoding, value))
    write(template % (encoding, value))

def unmarshall_int(self, data):
    self.append(int(data))
    self._value = 0

def unmarshall_binary(self, data):
    encoding, data = data.split(',', 1)

    data = codecs.decode(data, 'hex')

    if encoding in ('latin-1', 'utf-8'):
        data = data.decode(encoding)
    elif encoding == 'bytes':
        pass
    elif encoding == 'bytearray':
        data = bytearray(data)

    self.append(data)
    self._value = 0

# Registration routines
def register_integer_type(t):
    xmlrpclib.Marshaller.dispatch[t] = marshall_int

def register_binary_type(t):
    xmlrpclib.Marshaller.dispatch[t] = marshall_binary

# We make some changes to the XMLRPC spec to support our needs
register_integer_type(type(1))          # int
register_integer_type(type(1 << 100))   # python2 long

register_binary_type(type(''))  # Python2 strings
register_binary_type(type('🤖'))  # Unicode strings
register_binary_type(type(b'')) # Byte strings
register_binary_type(bytearray) # Byte arrays

xmlrpclib.Unmarshaller.dispatch['binary'] = unmarshall_binary
