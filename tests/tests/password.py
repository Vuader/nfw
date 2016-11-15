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
import logging
import unittest

import nfw

log = logging.getLogger(__name__)

class Password(unittest.TestCase):
    def test_hashing(self):
        algos = [ nfw.BLOWFISH,
                  nfw.MD5,
                  nfw.CLEARTEXT,
                  nfw.SHA256,
                  nfw.SHA512,
                  nfw.LDAP_MD5,
                  nfw.LDAP_SMD5,
                  nfw.LDAP_SHA1,
                  nfw.LDAP_SSHA1,
                  nfw.LDAP_CLEARTEXT,
                  nfw.LDAP_BLOWFISH,
                  nfw.LDAP_SHA256,
                  nfw.LDAP_SHA512
                  ]
        for algo in algos:
            if algo == nfw.CLEARTEXT or algo == nfw.LDAP_CLEARTEXT:
                pt = True
            else:
                pt = False
            hashed = nfw.password.hash('T0pS3cr3t!',algo, 10)
            valid = nfw.password.valid('T0pS3cr3t!', hashed, pt)
            self.assertEqual(valid, True)
