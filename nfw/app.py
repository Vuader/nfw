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

import os
import sys
import logging
import inspect
import io
from StringIO import StringIO
import urlparse
import cgi
import thread
from urllib import quote
import json
import traceback
import keyword
import re

from jinja2 import Environment as jinja2
from jinja2.exceptions import TemplateNotFound

import nfw

log = logging.getLogger(__name__)


class Wsgi(object):
    def __init__(self):
        if 'NEUTRINO_CONFIG' in os.environ:
            if os.path.isfile(os.environ['NEUTRINO_CONFIG']):
                nfw.config.nfw_config = os.environ['NEUTRINO_CONFIG']
            else:
                raise nfw.Error("Configuration file not found: %s"
                                % (os.environ['NEUTRINO_CONFIG'],))
        else:
            raise nfw.Error("Configuration file not found in os.environment")
        self.config = nfw.Config()
        app_config = self.config.get('application', {})
        log_config = self.config.get('logging', {})
        app_name = app_config.get('name','neutrino')
        host = log_config.get('host')
        port = log_config.get('port', 514)
        debug = log_config.get('debug', False)
        self.logger = nfw.Logger(app_name, host, port, debug)

        modules = app_config.getitems('modules')

        jinja = jinja2(loader=nfw.template.JinjaLoader(modules))
        jinja.globals['STATIC'] = app_config.get('static', '').rstrip('/')
        if jinja.globals['STATIC'] == '/':
            jinja.globals['STATIC'] = ''
        nfw.jinja = jinja

        middleware = app_config.getitems('middleware')
        self.router = nfw.Router()
        self.modules = self._modules()
        self.views = self._objs(self.modules, nfw.Resource)
        self.middleware = self._m_objs(self.modules, middleware)
        if os.path.isfile("policy.json"):
            policy = file("policy.json", 'r').read()
            self.policy = json.loads(policy)
        else:
            self.policy = None

    def _error_template(self, code):
        for module in self.modules:
            try:
                t = nfw.jinja.get_template("%s.html" % (code))
                return t
            except TemplateNotFound:
                pass
            try:
                t = nfw.jinja.get_template("%s/%s.html" % (module, code))
                return t
            except TemplateNotFound:
                pass

        return None

    def _error(self, e, resp):
        if hasattr(e, 'headers'):
            resp.headers.update(e.headers)

        if hasattr(e, 'status'):
            resp.status = e.status
        else:
            resp.status = nfw.HTTP_500

        if hasattr(e, 'code'):
            code = e.code
        else:
            code = resp.status.split(" ")[0]

        if hasattr(e, 'title'):
            title = e.title
        else:
            title = None

        if hasattr(e, 'description'):
            description = e.description
        else:
            description = repr(e)

        if resp.headers.get('Content-Type') == nfw.TEXT_PLAIN:
            resp.clear()
            if title is not None:
                resp.write("%s\n" % (title,))
            if description is not None:
                resp.write("%s" % (description,))
        elif resp.headers.get('Content-Type') == nfw.TEXT_HTML:
            t = self._error_template(code)
            if t is not None:
                resp.body = t.render(title=title, description=description)
            else:
                dom = nfw.web.Dom()
                html = dom.create_element('html')
                head = html.create_element('head')
                t = head.create_element('title')
                t.append(resp.status)
                body = html.create_element('body')
                if title is not None:
                    h1 = body.create_element('h1')
                    h1.append(title)
                if description is not None:
                    h2 = body.create_element('h2')
                    h2.append(description)
                resp.body = dom.get()
        elif resp.headers.get('Content-Type') == nfw.APPLICATION_JSON:
            j = {'error': {'title': title, 'description': description}}
            resp.body = nfw.utils.json_encode(j)

        return resp

    def _cleanup(self):
        nfw.Mysql.close_all()

    # The application interface is a callable object
    def _interface(self, environ, start_response):
        # environ points to a dictionary containing CGI like environment
        # variables which is populated by the server for each
        # received request from the client
        # start_response is a callback function supplied by the server
        # which takes the HTTP status and headers as arguments

        # When the method is POST the variable will be sent
        # in the HTTP request body which is passed by the WSGI server
        # in the file like wsgi.input environment variable.
        request_post = {}

        app_config = self.config.get('application', {})
        log_config = self.config.get('logging', {})
        debug = log_config.get('debug', False)
        session_expire = app_config.get('session_expire', 3600)

        if 'redis' in self.config:
            session = nfw.SessionRedis(session_expire)
        else:
            session = nfw.SessionFile(session_expire, 'tmp/')
        session_cookie = session.setup(environ)

        mysql_config = self.config.get('mysql', None)
        if mysql_config is not None:
            nfw.Mysql(**mysql_config.data)

        resp = nfw.Response()
        req = nfw.Request(environ, self.config, session, self.router, self.logger)

        resp.headers['Set-Cookie'] = session_cookie

        r = self.router.route(req)

        if debug is True:
            log.debug("Request URI: %s" % (req.get_full_path()))
            log.debug("Request QUERY: %s" % (req.environ['QUERY_STRING'],))

        response_headers = []

        if nfw.jinja is not None:
            nfw.jinja.globals['SITE'] = req.environ['SCRIPT_NAME']
            nfw.jinja.globals['REQUEST'] = req
            if nfw.jinja.globals['SITE'] == '/':
                jinja.globals['SITE'] = ''

        returned = None
        try:
            if r is not None:
                route, obj_kwargs = r
                method, route, obj, name = route
                req.args = obj_kwargs
                req.view = name
                policy = nfw.Policy(self.policy,
                                    context=req.context,
                                    session=req.session,
                                    kwargs=obj_kwargs,
                                    qwargs=req.query)
                req.policy = policy

            for m in self.middleware:
                if hasattr(m, 'pre'):
                    m.pre(req, resp)

            if r is not None:
                if policy.validate(req.view):
                    returned = obj(req, resp, **obj_kwargs)
                else:
                    raise nfw.HTTPForbidden('Access Forbidden',
                                            'Access denied by system policy')
            else:
                raise nfw.HTTPNotFound(description=req.environ['PATH_INFO'])

            for m in reversed(self.middleware):
                if hasattr(m, 'post'):
                    m.post(req, resp)

        except nfw.HTTPError as e:
            trace = str(traceback.format_exc())
            if debug is True:
                log.error("%s\n%s" % (e, trace))
            self._error(e, resp)
        except Exception as e:
            trace = str(traceback.format_exc())
            log.error("%s\n%s" % (e, trace))
            self._error(e, resp)

        resp.headers['X-Powered-By'] = 'Neutrino'
        resp.headers['X-Request-ID'] = req.request_id
        # HTTP headers expected by the client
        # They must be wrapped as a list of tupled pairs:
        # [(Header name, Header value)].
        for header in resp.headers:
            header = nfw.utils.if_unicode_to_utf8(header)
            value = nfw.utils.if_unicode_to_utf8(resp.headers[header])
            h = (header, value)
            response_headers.append(h)

        if returned is None:
            response_headers.append(('Content-Length'.encode('utf-8'),
                                     str(resp.content_length).encode('utf-8')))

        # Send status and headers to the server using the supplied function
        start_response(resp.status, response_headers)

        self._cleanup()

        if returned is not None:
            return returned
        else:
            return resp

    def _modules(self):
        app_config = self.config.get('application', {})
        loaded = {}
        modules = app_config.getitems('modules')
        for module in modules:
            try:
                m = nfw.utils.import_module(module)
                loaded[module] = m
            except Exception as e:
                trace = str(traceback.format_exc())
                log.error("Can't import module %s\n%s" % (str(e), trace))
        return loaded

    def _objs(self, modules, obj_type=nfw.Resource):
        loaded = []
        for module in modules:
            cls = inspect.getmembers(modules[module], inspect.isclass)
            for c in cls:
                if issubclass(c[1], obj_type):
                    try:
                        loaded.append(c[1](self))
                    except Exception as e:
                        trace = str(traceback.format_exc())
                        log.error("%s\n%s" % (str(e), trace))
        return loaded

    def _m_objs(self, modules, middleware):
        loaded = []
        for m in middleware:
            z = m.split('.')
            if len(z) > 1:
                l = len(z)
                mod = z[0:l-1]
                mod = '.'.join(mod)
                cls = z[l-1]
                if mod in modules:
                    mod = modules[mod]
                    if hasattr(mod, cls):
                        cls = getattr(mod, cls)
                        try:
                            loaded.append(cls(self))
                        except Exception as e:
                            trace = str(traceback.format_exc())
                            log.error("%s\n%s" % (str(e), trace))
                    else:
                        raise ImportError(m)
                else:
                    raise ImportError(m)
            else:
                raise ImportError(m)
        return loaded

    def application(self):
        # Return the application interface method as a callable object
        return self._interface
