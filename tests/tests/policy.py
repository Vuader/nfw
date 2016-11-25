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

import nfw

log = logging.getLogger(__name__)

class Policies(unittest.TestCase):
    def __init__(self, methodName):
        policy_file = (os.path.abspath(os.path.join(
                       os.path.dirname(__file__),
                       'policy.json')))
        policy_file = file(policy_file, 'r').read()
        policy = json.loads(policy_file)
        context = {}
        context['true'] = True
        context['false'] = False
        context['string'] = 'testing'
        session = {}
        obj_kwargs = {}
        get = {}
        self.policy = nfw.Policy(policy,
                            context=context,
                            session=session,
                            kwargs=obj_kwargs,
                            qwargs=get)
        super(Policies, self).__init__(methodName)

    def test_true(self):
        self.assertEqual(self.policy.validate('test:true'),True)

    def test_false(self):
        self.assertEqual(self.policy.validate('test:false'),False)

    def test_norule(self):
        self.assertEqual(self.policy.validate('test:norule'),False)

    def test_basic_true(self):
        self.assertEqual(self.policy.validate('test:basic_true'),True)

    def test_basic_true_or(self):
        self.assertEqual(self.policy.validate('test:basic_true_or'),True)

    def test_basic_true_and(self):
        self.assertEqual(self.policy.validate('test:basic_true_or'),True)

    def test_basic_false(self):
        self.assertEqual(self.policy.validate('test:basic_false'),False)

    def test_advanced_true1(self):
        self.assertEqual(self.policy.validate('test:advanced_true1'),True)

    def test_advanced_true2(self):
        self.assertEqual(self.policy.validate('test:advanced_true2'),True)

    def test_advanced_false1(self):
        self.assertEqual(self.policy.validate('test:advanced_false1'),False)

    def test_advanced_false2(self):
        self.assertEqual(self.policy.validate('test:advanced_false2'),False)

    def test_var_true(self):
        self.assertEqual(self.policy.validate('test:var_true'),True)

    def test_var_false(self):
        self.assertEqual(self.policy.validate('test:var_false'),False)

    def test_var_string(self):
        self.assertEqual(self.policy.validate('test:var_string'),True)
