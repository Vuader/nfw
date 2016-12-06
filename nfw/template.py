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
import logging
import traceback
import thread

from pkg_resources import DefaultProvider, ResourceManager, \
                          get_provider
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from jinja2.utils import open_if_exists, internalcode
from jinja2._compat import string_types, iteritems
from jinja2.loaders import BaseLoader
from jinja2 import loaders

import nfw

log = logging.getLogger(__name__)

class Jinja(object):
    def __init__(self):
        self._threads = {}
        self.config = nfw.Config()
        self.app_config = self.config.get('application')
        self.modules = self.app_config.getitems('modules')
        self._globals = {}

    def setup(self):
        thread_id = thread.get_ident()
        if thread_id not in self._threads:
            self._threads[thread_id] = Environment(loader=nfw.template.JinjaLoader(self.modules))
            self._threads[thread_id].globals.update(self._globals)
            self._threads[thread_id].globals['STATIC'] = self.app_config.get('static', '').rstrip('/')
            if self._threads[thread_id].globals['STATIC'] == '/':
                 self._threads[thread_id].globals['STATIC'] = ''

    def __getattr__(self, attr):
        thread_id = thread.get_ident()
        if thread_id in self._threads:
            if hasattr(self._threads[thread_id], attr):
                return getattr(self._threads[thread_id], attr)
            else:
                raise Exception("Jinja Environment has no attribute %s" % (attr,))
        else:
            if attr == 'globals':
                return self._globals
            else:
                raise Exception("Jinja not loaded yet for thread")

class JinjaLoader(BaseLoader):
    def __init__(self, packages):
        self.searchpath = ['templates']
        try:
            self.fsl = loaders.FileSystemLoader(self.searchpath)
        except Exception as e:
            log.error(e)

        self.packages = {}
        self.encoding = 'utf-8'
        self.package_path = "templates"
        self.manager = ResourceManager()
        for package_name in packages:
            try:
                pkg = self.packages[package_name] = {}
                pkg['provider'] = get_provider(package_name)
                pkg['fs_bound'] = isinstance(pkg['provider'], DefaultProvider)
            except Exception as e:
                trace = str(traceback.format_exc())
                log.error("Can't import module %s\n%s" % (str(e), trace))

    def get_source(self, environment, template):
        pieces = loaders.split_template_path(template)
        try:
            return self.fsl.get_source(environment, template)
        except Exception as e:
            pass

        if len(pieces) > 1 and pieces[0] in self.packages:
            pkg_name = pieces[0]
            pkg = self.packages[pkg_name]
            del pieces[0]
            p = '/'.join((self.package_path,) + tuple(pieces))
            if not pkg['provider'].has_resource(p):
                raise TemplateNotFound(template)
        else:
            raise TemplateNotFound(template)

        filename = uptodate = None
        if pkg['fs_bound']:
            filename = pkg['provider'].get_resource_filename(self.manager, p)
            mtime = os.path.getmtime(filename)

            def uptodate():
                try:
                    return os.path.getmtime(filename) == mtime
                except OSError:
                    return False

        source = pkg['provider'].get_resource_string(self.manager, p)
        return source.decode(self.encoding), filename, uptodate

    def list_templates(self):
        fsl = []
        try:
            fsl = self.fsl.get_source(environment, template)
        except Exception as e:
            log.error(e)

        path = self.package_path
        if path[:2] == './':
            path = path[2:]
        elif path == '.':
            path = ''
        offset = len(path)
        results = []

        def _walk(path):
            for package_name in self.packages:
                pkg = self.packages[package_name]
                for filename in pkg['provider'].resource_listdir(path):
                    fullname = path + '/' + filename
                    if pkg['provider'].resource_isdir(fullname):
                        _walk(fullname)
                    else:
                        p = fullname[offset:].lstrip('/')
                        p = "%s/%s" % (package_name, p)
                        results.append(p)
        _walk(path)
        results.sort()

        return results + fsl
