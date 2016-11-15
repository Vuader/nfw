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

import sys
import logging

import nfw


class _Constant(object):
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind constant(%s)" % name)
        self.__dict__[name] = value

_const = _Constant()

# CONSTANTS
_const.TEXT_HTML = 'text/html; charset=UTF-8'.encode('utf-8')
_const.TEXT_PLAIN = 'text/plain; charset=UTF-8'.encode('utf-8')
_const.TEXT_CSS = 'text/css; charset=UTF-8'.encode('utf-8')
_const.IMAGE_JPEG = 'image/jpeg'.encode('utf-8')
_const.IMAGE_GIF = 'image/gif'.encode('utf-8')
_const.IMAGE_PNG = 'image/png'.encode('utf-8')
_const.APPLICATION_XML = 'application/xml; charset=UTF-8'.encode('utf-8')
_const.APPLICATION_JSON = 'application/json; charset=UTF-8'.encode('utf-8')
_const.APPLICATION_OCTET_STREAM = 'application/octet-stream'.encode('utf-8')

_const.HTTP_GET = "GET"
_const.HTTP_POST = "POST"
_const.HTTP_PUT = "PUT"
_const.HTTP_DELETE = "DELETE"

_const.HTTP_100 = '100 Continue'.encode('utf-8')
_const.HTTP_101 = '101 Switching Protocols'.encode('utf-8')
_const.HTTP_200 = '200 OK'.encode('utf-8')
_const.HTTP_201 = '201 Created'.encode('utf-8')
_const.HTTP_202 = '202 Accepted'.encode('utf-8')
_const.HTTP_203 = '203 Non-Authoritative Information'.encode('utf-8')
_const.HTTP_204 = '204 No Content'.encode('utf-8')
_const.HTTP_205 = '205 Reset Content'.encode('utf-8')
_const.HTTP_206 = '206 Partial Content'.encode('utf-8')
_const.HTTP_226 = '226 IM Used'.encode('utf-8')
_const.HTTP_300 = '300 Multiple Choices'.encode('utf-8')
_const.HTTP_301 = '301 Moved Permanently'.encode('utf-8')
_const.HTTP_302 = '302 Found'.encode('utf-8')
_const.HTTP_303 = '303 See Other'.encode('utf-8')
_const.HTTP_304 = '304 Not Modified'.encode('utf-8')
_const.HTTP_305 = '305 Use Proxy'.encode('utf-8')
_const.HTTP_307 = '307 Temporary Redirect'.encode('utf-8')
_const.HTTP_400 = '400 Bad Request'.encode('utf-8')
_const.HTTP_401 = '401 Unauthorized'.encode('utf-8')  # <-- Really means "unauthenticated"
_const.HTTP_402 = '402 Payment Required'.encode('utf-8')
_const.HTTP_403 = '403 Forbidden'.encode('utf-8')  # <-- Really means "unauthorized"
_const.HTTP_404 = '404 Not Found'.encode('utf-8')
_const.HTTP_405 = '405 Method Not Allowed'.encode('utf-8')
_const.HTTP_406 = '406 Not Acceptable'.encode('utf-8')
_const.HTTP_407 = '407 Proxy Authentication Required'.encode('utf-8')
_const.HTTP_408 = '408 Request Time-out'.encode('utf-8')
_const.HTTP_409 = '409 Conflict'.encode('utf-8')
_const.HTTP_410 = '410 Gone'.encode('utf-8')
_const.HTTP_411 = '411 Length Required'.encode('utf-8')
_const.HTTP_412 = '412 Precondition Failed'.encode('utf-8')
_const.HTTP_413 = '413 Payload Too Large'.encode('utf-8')
_const.HTTP_414 = '414 URI Too Long'.encode('utf-8')
_const.HTTP_415 = '415 Unsupported Media Type'.encode('utf-8')
_const.HTTP_416 = '416 Range Not Satisfiable'.encode('utf-8')
_const.HTTP_417 = '417 Expectation Failed'.encode('utf-8')
_const.HTTP_418 = "418 I'm a teapot".encode('utf-8')
_const.HTTP_422 = "422 Unprocessable Entity".encode('utf-8')
_const.HTTP_426 = '426 Upgrade Required'.encode('utf-8')
_const.HTTP_428 = '428 Precondition Required'.encode('utf-8')
_const.HTTP_429 = '429 Too Many Requests'.encode('utf-8')
_const.HTTP_431 = '431 Request Header Fields Too Large'.encode('utf-8')
_const.HTTP_451 = '451 Unavailable For Legal Reasons'.encode('utf-8')
_const.HTTP_500 = '500 Internal Server Error'.encode('utf-8')
_const.HTTP_501 = '501 Not Implemented'.encode('utf-8')
_const.HTTP_502 = '502 Bad Gateway'.encode('utf-8')
_const.HTTP_503 = '503 Service Unavailable'.encode('utf-8')
_const.HTTP_504 = '504 Gateway Time-out'.encode('utf-8')
_const.HTTP_505 = '505 HTTP Version not supported'.encode('utf-8')
_const.HTTP_511 = '511 Network Authentication Required'.encode('utf-8')

_const.BLOWFISH = 1
_const.MD5 = 2
_const.SHA256 = 3
_const.SHA512 = 4
_const.CLEARTEXT = 5
_const.LDAP_BLOWFISH = 6
_const.LDAP_MD5 = 7
_const.LDAP_SMD5 = 8
_const.LDAP_SHA1 = 9
_const.LDAP_SSHA1 = 10
_const.LDAP_SHA256 = 11
_const.LDAP_SHA512 = 12
_const.LDAP_CLEARTEXT = 13

_const.LEFT = 1
_const.RIGHT = 2

sys.modules[__name__] = _const
