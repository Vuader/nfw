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

import datetime
import string
import random
import sys


def import_module(module):
    #if sys.version_info[0] == 2:
        #module = __import__(module, globals(), locals(), ['object'], -1)
        #return module
    __import__(module)
    return sys.modules[module]


class ObjectName(object):
    def _objectname(o):
        return o.__module__ + "." + o.__class__.__name__


def timer(started=None, pretty=False):
    if started is None:
        return datetime.datetime.now()
    else:
        seconds = (datetime.datetime.now()-started).total_seconds()
        if pretty is False:
            if seconds > 0.0001:
                return seconds
            else:
                return 0
        else:
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            return "%d:%02d:%02d" % (h, m, s)


def random_id(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def if_unicode_to_utf8(string):
    if sys.version_info[0] == 2:
        if isinstance(string, unicode):
            return string.encode('utf-8')
        else:
            return string
    else:
        if isinstance(string, str):
            return string.encode('utf-8')
        else:
            return string

def is_byte_string(string):
    if sys.version_info[0] == 2:
        if isinstance(string, str):
            return True
        else:
            return False
    else:
        if isinstance(string, bytes):
            return True
        else:
            return False
