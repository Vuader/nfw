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
import os
import logging
import unittest
import json
from StringIO import StringIO

import nfw

log = logging.getLogger(__name__)

class Routes(unittest.TestCase):
    def __init__(self, methodName):
        self.router = nfw.Router()
        self.config = {}
        self.session = {}
        self.logger = nfw.Logger('test', None, None, False)
        self.environ = {}
        self.environ['REQUEST_METHOD'] = None
        self.environ['PATH_INFO'] = None
        self.environ['SCRIPT_NAME'] = '/test'
        self.environ['REMOTE_ADDR'] = '127.0.0.1'
        self.environ['wsgi.input'] = StringIO()
        self.environ['QUERY_STRING'] = ''
        self.req = nfw.Request(self.environ, self.config, self.session, self.router, self.logger)
        self.resp = nfw.Response()

        super(Routes, self).__init__(methodName)

    def view(self, req, resp, **kwargs):
        self.resp.body = 'test'
        return kwargs

    def route(self, method, url, name, kwargs):
        self.req.method = method
        self.environ['PATH_INFO'] = url
        self.req.view = name
        self.req.method = method
        r = self.router.route(self.req)
        route, obj_kwargs = r
        method, route, obj, r_name = route
        self.req.args = obj_kwargs
        returned = obj(self.req, self.resp, **obj_kwargs)
        self.resp.seek(0)
        response_body = self.resp.read()
        self.assertEqual(response_body, 'test')
        self.assertEqual(len(returned), len(kwargs))
        self.assertEqual(name, r_name)

        for k in returned:
            if k in kwargs:
                self.assertEqual(returned[k], kwargs[k])
            else:
                raise Exception('Too many kwargs attributes in route')

    def test_get(self):
        self.router.add(nfw.HTTP_GET, '/', self.view, 'get:get')
        kwargs = {}
        r = self.route(nfw.HTTP_GET, '/', 'get:get', kwargs)

        self.router.add(nfw.HTTP_GET, '/get_test', self.view, 'get_test:get_test')
        kwargs = {}
        r = self.route(nfw.HTTP_GET, '/get_test', 'get_test:get_test', kwargs)

    def test_post(self):
        self.router.add(nfw.HTTP_POST, '/post_test', self.view, 'post_test:post_test')
        kwargs = {}
        r = self.route(nfw.HTTP_POST, '/post_test', 'post_test:post_test', kwargs)

    def test_kwargs(self):
        self.router.add(nfw.HTTP_PUT, '/kwargs/{var1}/{var2}', self.view, 'kwargs_test:kwargs_test')
        kwargs = {'var1': 'test1', 'var2': 'test2'}
        r = self.route(nfw.HTTP_PUT, '/kwargs/test1/test2', 'kwargs_test:kwargs_test', kwargs)
