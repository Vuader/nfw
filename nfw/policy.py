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

import re
import logging

import nfw

log = logging.getLogger(__name__)


class Policy(object):
    def __init__(self, policy, **kwargs):
        self.kwargs = kwargs

        if policy is not None:
            self.policy = policy
        else:
            self.policy = None

    def _tokenize(self, rule):
        tokens = []
        t = ""
        rule = ' '.join(rule.split())
        for i in rule:
            if i == ' ':
                tokens.append(t)
                t = ""
            elif i == '(':
                if t != '':
                    tokens.append(t)
                tokens.append('(')
                t = ""
            elif i == ')':
                if t != '':
                    tokens.append(t)
                tokens.append(')')
                t = ""
            else:
                t += i
        if t != '':
            tokens.append(t)

        return tokens

    def _value(self, v):
        if v[0] == '$':
            if len(v) > 1:
                v = v[1:]
                if '.' in v:
                    d, k = v.split('.')
                    if d in self.kwargs:
                        d = self.kwargs[d]
                        if k in d:
                            return str(d[k])
            return None
        else:
            return v

    def _cmp(self, t):
        if t.lower() == "true":
            return True
        if t.lower() == "false":
            return False

        t = t.split(':')
        if len(t) == 2:
            x, y = t
            if x.lower() == 'rule':
                if y in self.policy:
                    return self._parse(self.policy[y])
                else:
                    raise DoesNotExist(str("name '%s' is not defined (policy)" % (y,)))
            else:
                x = self._value(x)
                y = self._value(y)
                if x is None or y is None:
                    return False
                if x == y:
                    return True
        return False

    def _parse(self, rule):
        if isinstance(rule, str) or isinstance(rule, unicode):
            rules = re.findall(r'\(([^{}]+)\)', rule, re.MULTILINE)
        if len(rules) == 0:
            return self._rule(rule)

        for r in rules:
            v = self._parse(r)
            r = "(%s)" % (r,)
            rule = rule.replace(r, str(v))
        return self._rule(rule)

    def _rule(self, rule):
        lv = False
        op = None
        for t in self._tokenize(rule):
            if ':' in t or t.lower() == "true" or t.lower() == "false":
                if op is None:
                    lv = self._cmp(t)
                else:
                    if op == 'or':
                        lv += self._cmp(t)
                    if op == 'and':
                        lv = bool(lv * self._cmp(t))
            else:
                if t.lower() == 'or':
                    op = 'or'
                if t.lower() == 'and':
                    op = 'and'
        return bool(lv)

    def validate(self, view):
        if self.policy is not None:
            if view in self.policy:
                t = self._parse(self.policy[view])
                return t
        else:
            return True
        return False
