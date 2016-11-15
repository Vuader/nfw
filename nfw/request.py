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

import logging
import io
import urlparse
import cgi
from urllib import quote

import nfw

log = logging.getLogger(__name__)


class Request(object):
    def __init__(self, environ, config, session, router, logger):
        super(Request, self).__setattr__('context', {})
        super(Request, self).__setattr__('config', config)
        super(Request, self).__setattr__('router', router)
        super(Request, self).__setattr__('logger', logger)
        super(Request, self).__setattr__('session', session)
        super(Request, self).__setattr__('environ', environ)
        super(Request, self).__setattr__('method', environ['REQUEST_METHOD'])
        super(Request, self).__setattr__('app', environ['SCRIPT_NAME'])
        super(Request, self).__setattr__('headers', nfw.Headers())
        super(Request, self).__setattr__('request_id', nfw.random_id(16))

        self.logger.set_extra('(REQUEST:%s)' % (self.request_id))
        self.logger.append_extra('(REMOTE_ADDR:%s)' % (self.environ['REMOTE_ADDR']))
        script_filename = self.environ.get('SCRIPT_FILENAME', 'None')
        self.logger.append_extra('(WSGI:%s)' % (script_filename,))

        for p in environ:
            n = p.replace('.', '_').lower()
            if len(p) > 5 and 'HTTP_' in p:
                hk = p.replace('HTTP_', '')
                self.headers[hk] = environ[p]
        try:
            super(Request, self).__setattr__('content_length',
                                             int(environ.get('CONTENT_LENGTH',
                                                 0)))
            self._input = environ['wsgi.input']
        except (ValueError):
            super(Request, self).__setattr__('content_length', 0)
            self._input = None

        self._read_field = False
        self._read_file = False
        self._post = None
        get = urlparse.parse_qs(self.environ['QUERY_STRING'])
        super(Request, self).__setattr__('get', get)

    def __setattr__(self, name, value):
        if name == 'method':
            super(Request, self).__setattr__(name, value.upper())
        elif name[0] == '_':
            super(Request, self).__setattr__(name, value)
        elif hasattr(self, name):
            raise AttributeError("'request' object can't rebind" +
                                 " attribute '%s'" % (name,))
        elif name == 'args' or name == 'view' or name == 'policy':
            super(Request, self).__setattr__(name, value)
        else:
            raise AttributeError("'request' object can't bind" +
                                 " attribute '%s'" % (name,))

    def __getattr__(self, name):
        name = name.lower()
        if name in self.__dict__:
            return self.__dict__[name]
        elif name == 'post':
            if self._post is None:
                if self._read_file is False:
                    self._post = Post(self._input, self.environ)
                else:
                    raise Exception("'You cannot use post after" +
                                    " reading from body'")
            return self._post
        else:
            raise AttributeError("'request' object has no" +
                                 " attribute '%s'" % (name,))

    def read(self, size=io.DEFAULT_BUFFER_SIZE):
        if self._read_field is False:
            if self._input is not None:
                self._read_file = True
                return self._input.read(size)
        else:
            raise Exception("'You cannot read from body after accessing post'")

    def readline(self, size=io.DEFAULT_BUFFER_SIZE):
        if self._read_field is False:
            if self._input is not None:
                self._read_file = True
                return self._input.readline(size)
        else:
            raise Exception("'You cannot read from body after accessing post'")

    def get_host(self):
        config = nfw.Config()
        app_config = config.get('application', {})
        use_x_forwarded_host = app_config.get('use_x_forwarded_host', False)
        if use_x_forwarded_host is True and 'X_FORWARDED_HOST' in self.headers:
            return self.headers['X_FORWARDED_HOST']
        elif 'HOST' in self.headers:
            return self.headers['HOST']
        elif 'SERVER_NAME' in self.environ:
            return self.environ['SERVER_NAME']
        elif 'SERVER_ADDR' in self.environ:
            return self.environ['SERVER_ADDR']
        else:
            return '127.0.0.1'

    def get_port(self):
        config = nfw.Config()
        app_config = config.get('application', {})
        use_x_forwarded_port = app_config.get('use_x_forwarded_port', False)
        port = None
        if use_x_forwarded_port is True and 'X_FORWARDED_PORT' in self.headers:
            return self.headers['X_FORWARDED_PORT']
        elif 'SERVER_PORT' in self.environ:
            return self.environ['SERVER_PORT']

    def get_proto(self):
        return self.environ['wsgi.url_scheme']

    def get_script(self):
        if 'SCRIPT_NAME' in self.environ:
            return self.environ['SCRIPT_NAME']
        else:
            return None

    def get_app(self):
        return self.get_script()

    def get_full_path(self):
        url = quote(self.get_script())
        if 'PATH_INFO' in self.environ:
            url += quote(self.environ['PATH_INFO'])
        if 'QUERY_STRING' in self.environ:
            url += '?' + self.environ['QUERY_STRING']

        return url

    def get_app_url(self):
        url = self.get_proto()+'://'
        url += self.get_host()

        if self.get_proto() == 'https':
            if self.get_port() != '443':
                url += ':' + self.get_port
        elif self.get_proto() == 'http':
            if self.get_port() != '80':
                url += ':' + self.get_port

        url += quote(self.get_script())

        return url

    def get_absolute_url(self):
        url = self.get_proto()+'://'
        url += self.get_host()

        if self.get_proto() == 'https':
            if self.get_port() != '443':
                url += ':' + self.get_port
        elif self.get_proto() == 'http':
            if self.get_port() != '80':
                url += ':' + self.get_port

        url += quote(self.get_script())
        if 'PATH_INFO' in self.environ:
            url += quote(self.environ['PATH_INFO'])
        if 'QUERY_STIRNG' in self.environ:
            url += '?' + self.environ['QUERY_STRING']

        return url

    def is_secure(self):
        if self.get_proto() == 'https':
            return True
        else:
            return False

    def is_ajax(self):
        if ('X_REQUESTED_WITH' in self.headers and
                'xmlhttprequest' in self.headers['X_REQUESTED_WITH'].lower()):
            return True
        else:
            return False

    def is_mobile(self):
        # HTTP_USER_AGENT
        agent = self.headers.get('user_agent', '').lower()
        if 'iphone' in agent:
            return True
        elif 'android' in agent:
            return True
        else:
            return False

    def is_bot(self):
        # HTTP_USER_AGENT
        agent = self.headers.get('user_agent', '').lower()
        if 'google' in agent:
            return True
        elif 'bingbot' in agent:
            return True
        elif 'msnbot' in agent:
            return True
        elif 'adidxbot' in agent:
            return True
        elif 'bingpreview' in agent:
            return True
        elif 'yandex' in agent:
            return True
        elif 'yahoo' in agent:
            return True
        elif 'slurp' in agent:
            return True
        elif 'baidu' in agent:
            return True
        else:
            return False


class Post(object):
    def __init__(self, fp, environ):
        self._cgi = cgi.FieldStorage(fp=fp, environ=environ)

    def __getitem__(self, key):
        return self._cgi[key]

    def __contains__(self, key):
        return key in self._cgi

    def __iter__(self):
        return iter(self._cgi)
