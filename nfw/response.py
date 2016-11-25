# Neutrino Framework
#
# Copyright (c) 2016, Christiaan Frans Rademan
# All rights reserved.
#
# LICENSE: (BSD3-Clause)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENTSHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import logging
from StringIO import StringIO

import nfw

log = logging.getLogger(__name__)


class Response(object):
    _attributes = ['status']

    def __init__(self):
        self.status = nfw.HTTP_200
        super(Response, self).__setattr__('headers', nfw.Headers())
        self.headers['Content-Type'] = nfw.TEXT_HTML
        super(Response, self).__setattr__('_io', StringIO())
        super(Response, self).__setattr__('content_length', 0)
        self.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        self.headers['Progma'] = 'no-cache'
        self.headers['Expires'] = 0

    def __setattr__(self, name, value):
        if name in self._attributes:
            super(Response, self).__setattr__(name, value)
        elif name == 'body':
            self.clear()
            super(Response, self).__setattr__('content_length', len(value))
            super(Response, self).__setattr__('_io', StringIO())
            self.write(value)
        else:
            AttributeError("'response' object can't bind" +
                           " attribute '%s'" % (name,))

    def seek(self,position):
        self._io.seek(position)

    def read(self, size=io.DEFAULT_BUFFER_SIZE):
        return self._io.read(size)

    def readline(self, size=io.DEFAULT_BUFFER_SIZE):
        return self._io.readline(size)

    def write(self, data):
        super(Response, self).__setattr__('content_length',
                                          len(data)+self.content_length)
        self._io.write(data)

    def clear(self):
        super(Response, self).__setattr__('_io', StringIO())

    def __iter__(self):
        self._io.seek(0)
        return ResponseIoStream(self._io)


def ResponseIoStream(f, chunk_size=None):
    '''Genereator to buffer chunks'''
    while True:
        if chunk_size is None:
            chunk = f.read()
        else:
            chunk = f.read(chunk_size)
        if not chunk:
            break
        yield nfw.utils.if_unicode_to_utf8(chunk)
