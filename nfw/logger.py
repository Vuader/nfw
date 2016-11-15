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
import os
import stat
import logging
import logging.handlers
import inspect
import time
import thread

import nfw


class Logger(object):
    def _is_socket(self, socket):
        try:
            mode = os.stat(socket).st_mode
            is_socket = stat.S_ISSOCK(mode)
        except:
            is_socket = False
        return is_socket

    class _Filter(logging.Filter):
        def __init__(self, debug=False, get_extra=None):
            logging.Filter.__init__(self)
            self.debug = debug
            self._get_extra = get_extra

        def filter(self, record):
            if self._get_extra is not None:
                record.extra = self._get_extra()
            if record.levelno == logging.DEBUG:
                return self.debug
            return True

    def set_extra(self, value):
        thread_id = thread.get_ident()
        self._request[thread_id] = []
        self._request[thread_id].append(value)

    def append_extra(self, value):
        thread_id = thread.get_ident()
        if thread_id not in self._request:
            self._request[thread_id] = []
        self._request[thread_id].append(value)

    def _get_extra(self):
        thread_id = thread.get_ident()
        if thread_id in self._request:
            return " ".join(self._request[thread_id])
        else:
            return ""

    def __init__(self, app_name, host, port, debug):
        self._request = {}

        logger = logging.getLogger()

        logger.setLevel(logging.DEBUG)

        if host is not None and (host == '127.0.0.1' or host == 'localhost'):
            if self._is_socket('/dev/log'):
                syslog = logging.handlers.SysLogHandler(address='/dev/log')
            elif self._is_socket('/var/run/syslog'):
                syslog = logging.handlers.SysLogHandler(address='/var/run/syslog')
            else:
                syslog = logging.handlers.SysLogHandler(address=(host, port))
        else:
            if host is not None:
                syslog = logging.handlers.SysLogHandler(address=(host, port))

        stdout = logging.StreamHandler()

        log_format = logging.Formatter('%(asctime)s ' + app_name +
                                       ' %(name)s[' + str(os.getpid()) + ']' +
                                       ' <%(levelname)s>: %(message)s %(extra)s',
                                       datefmt='%b %d %H:%M:%S')

        if host is not None:
            syslog.formatter = log_format
            logger.addHandler(syslog)
        stdout.formatter = log_format
        logger.addHandler(stdout)

        for handler in logging.root.handlers:
            handler.addFilter(self._Filter(debug=debug, get_extra=self._get_extra))
