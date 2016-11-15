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
import base64
import pickle
import time
import datetime
from Cookie import SimpleCookie

import nfw

log = logging.getLogger(__name__)


class SessionBase(object):
    def __init__(self, expire=3600):
        self._name = None
        self._expire = expire
        self._id = None

    def setup(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

        cookie = SimpleCookie()
        name = nfw.utils.if_unicode_to_utf8('neutrino')

        if 'HTTP_COOKIE' in self.environ:
            cookie.load(self.environ['HTTP_COOKIE'])
        if name in cookie:
            id = nfw.utils.if_unicode_to_utf8(cookie[name].value)
        else:
            id = nfw.utils.if_unicode_to_utf8(nfw.random_id(16))

        self._id = nfw.utils.if_unicode_to_utf8(id)
        self._name = "session:%s" % (id,)
        cookie[name] = nfw.utils.if_unicode_to_utf8(id)
        cookie_string = cookie[name].OutputString()
        return cookie_string


class SessionRedis(SessionBase):
    def __setitem__(self, key, value):
        nfw.redis.hset(self._name, key, value)
        nfw.redis.expire(self._name, self._expire)

    def __getitem__(self, key):
        val = nfw.redis.hget(self._name, key)
        if val == 'True':
            return True
        elif val == 'False':
            return False
        else:
            return val

    def __delitem__(self, key):
        nfw.redis.hdel(self._name, key)

    def __contains__(self, key):
        return nfw.redis.hexists(self._name, key)

    def __iter__(self):
        return iter(nfw.redis.hgetall(self._name))

    def __len__(self):
        return hlen(nfw.redis.hlen(self._name))

    def get(self, k, d=None):
        if k in self:
            val = nfw.redis.hget(self._name, k)
            if val == 'True':
                return True
            elif val == 'False':
                return False
            else:
                return val
        else:
            return d


class SessionFile(SessionBase):
    def _load(self):
        if os.path.isfile("tmp/%s.session" % (self._id,)):
            ts = int(time.mktime(datetime.datetime.now().timetuple()))
            stat = os.stat("tmp/%s.session" % (self._id))
            lm = int(stat.st_mtime)
            if ts - lm > self._expire:
                self._session = {}

        if not hasattr(self, '_session'):
            if os.path.isfile("tmp/%s.session" % (self._id,)):
                with open("tmp/%s.session" % (self._id,), 'rb') as handle:
                    self._session = pickle.load(handle)
            else:
                self._session = {}

    def _save(self):
        with open("tmp/%s.session" % (self._id,), 'wb') as handle:
            pickle.dump(self._session, handle)

    def __setitem__(self, key, value):
        self._load()
        self._session[key] = value
        self._save()

    def __getitem__(self, key):
        self._load()
        return self._session[key]

    def __delitem__(self, key):
        self._load()
        try:
            del self._session[key]
            self._save()
        except KeyError:
            pass

    def __contains__(self, key):
        self._load()
        return key in self._session

    def __iter__(self):
        self._load()
        return iter(self._session)

    def __len__(self):
        self._load()
        return len(self._session)

    def get(self, k, d=None):
        self._load()
        return self._session.get(k, d)
