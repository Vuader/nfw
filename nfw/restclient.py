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
import logging
import sys
import os
import re
import thread

try:
    # python 3
    from io import BytesIO
except ImportError:
    # python 2
    from StringIO import StringIO as BytesIO
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

import pycurl

import nfw

log = logging.getLogger(__name__)

curl_sessions = {}

class RestClient(object):
    def __init__(self):
        global curl_sessions

        self.thread_id = thread.get_ident()
        if self.thread_id not in curl_sessions:
            curl_sessions[self.thread_id] = {}
        self.curl_session = curl_sessions[self.thread_id]

    def header_function(self,header_line):
        # HTTP standard specifies that headers are encoded in iso-8859-1.
        # On Python 2, decoding step can be skipped.
        # On Python 3, decoding step is required.
        header_line = header_line.decode('iso-8859-1')

        # Header lines include the first status line (HTTP/1.x ...).
        # We are going to ignore all lines that don't have a colon in them.
        # This will botch headers that are split on multiple lines...
        if ':' not in header_line:
            return

        # Break the header line into header name and value.
        name, value = header_line.split(':', 1)

        # Remove whitespace that may be present.
        # Header lines include the trailing newline, and there may be whitespace
        # around the colon.
        name = name.strip()
        value = value.strip()

        # Header names are case insensitive.
        # Lowercase name here.
        name = name.lower()

        # Now we can actually record the header name and value.
        self.server_headers[name] = value

    def get_host_port_from_url(self,url):
        url_splitted = url.split('/')
        host = "%s//%s" % (url_splitted[0],url_splitted[2])
        return host

    def execute(self,request,url,data=None,client_headers=None):
        host = self.get_host_port_from_url(url)
        if host in self.curl_session:
            curl = self.curl_session[host]
        else:
            self.curl_session[host] = pycurl.Curl()
            curl = self.curl_session[host]

        url = url.replace(" ","%20")

        request = request.lower()

        self.server_headers = dict()

        buffer = BytesIO()

        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, buffer)
        curl.setopt(curl.HEADERFUNCTION, self.header_function)
        curl.setopt(curl.FOLLOWLOCATION, True)
        curl.setopt(curl.SSL_VERIFYPEER, 0)
        curl.setopt(curl.SSL_VERIFYHOST, 0)
        curl.setopt(curl.CONNECTTIMEOUT, 2)

        if data is not None:
            curl.setopt(curl.POSTFIELDS, data)
        else:
            curl.setopt(curl.POSTFIELDS, '')

        send_headers = list()
        for header in client_headers:
            send_header = "%s: %s" % (header, client_headers[header])
            send_headers.append(send_header)

        curl.setopt(pycurl.HTTPHEADER, send_headers)

        if request == "get":
            curl.setopt(curl.CUSTOMREQUEST, 'GET')
        elif request == "put":
            curl.setopt(curl.CUSTOMREQUEST, 'PUT')
        elif request == "post":
            curl.setopt(curl.CUSTOMREQUEST, 'POST')
        elif request == "patch":
            curl.setopt(curl.CUSTOMREQUEST, 'PATCH')
        elif request == "delete":
            curl.setopt(curl.CUSTOMREQUEST, 'DELETE')
        else:
            raise nfw.Error("Invalid request type %s" % (request,))

        curl.perform()

        # Figure out what encoding was sent with the response, if any.
        # Check against lowercased header name.
        encoding = None
        if 'content-type' in self.server_headers:
            content_type = self.server_headers['content-type'].lower()
            match = re.search('charset=(\S+)', content_type)
            if match:
                encoding = match.group(1)
        if encoding is None:
            # Default encoding for HTML is iso-8859-1.
            # Other content types may have different default encoding,
            # or in case of binary data, may have no encoding at all.
            encoding = 'iso-8859-1'

        body = buffer.getvalue()
        # Decode using the encoding we figured out.
        body = body.decode(encoding)

        return (self.server_headers,body)

    def close_all(self):
        for session in self.session:
            self.session[session].close()

