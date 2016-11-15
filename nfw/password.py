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
import hashlib

import nfw
import bcrypt
import passlib.hash
import passlib.context

log = logging.getLogger(__name__)


def hash(password, algo=nfw.BLOWFISH, rounds=15):
    if (rounds < 1000 and
            (algo == nfw.SHA256 or
             algo == nfw.SHA512 or
             algo == nfw.LDAP_SHA256 or
             algo == nfw.LDAP_SHA512)):
        rounds = 1000

    if algo == nfw.BLOWFISH:
        hashed = passlib.hash.bcrypt.encrypt(password, rounds=rounds)
        return hashed
    elif algo == nfw.CLEARTEXT:
        return password
    elif algo == nfw.MD5:
        hashed = passlib.hash.md5_crypt.encrypt(password)
        return hashed
    elif algo == nfw.SHA256:
        hashed = passlib.hash.sha256_crypt.encrypt(password, rounds=rounds)
        return hashed
    elif algo == nfw.SHA512:
        hashed = passlib.hash.sha512_crypt.encrypt(password, rounds=rounds)
        return hashed
    elif algo == nfw.LDAP_MD5:
        hashed = passlib.hash.ldap_md5.encrypt(password)
        return hashed
    elif algo == nfw.LDAP_SMD5:
        hashed = passlib.hash.ldap_salted_md5.encrypt(password)
        return hashed
    elif algo == nfw.LDAP_SHA1:
        hashed = passlib.hash.ldap_sha1.encrypt(password)
        return hashed
    elif algo == nfw.LDAP_SSHA1:
        hashed = passlib.hash.ldap_salted_sha1.encrypt(password)
        return hashed
    elif algo == nfw.LDAP_CLEARTEXT:
        hashed = passlib.hash.ldap_plaintext.encrypt(password)
        return hashed
    elif algo == nfw.LDAP_BLOWFISH:
        hashed = passlib.hash.ldap_bcrypt.encrypt(password, rounds=rounds)
        return hashed
    elif algo == nfw.LDAP_SHA256:
        hashed = passlib.hash.ldap_sha256_crypt.encrypt(password,
                                                        rounds=rounds)
        return hashed
    elif algo == nfw.LDAP_SHA512:
        hashed = passlib.hash.ldap_sha512_crypt.encrypt(password,
                                                        rounds=rounds)
        return hashed
    else:
        pass


def valid(password, hashed, plaintext=False):
    pwd_context = passlib.context.CryptContext(schemes=["md5_crypt",
                                                        "bcrypt",
                                                        "sha256_crypt",
                                                        "sha512_crypt",
                                                        "ldap_md5",
                                                        "ldap_salted_md5",
                                                        "ldap_sha1",
                                                        "ldap_salted_sha1",
                                                        "ldap_bcrypt",
                                                        "ldap_sha256_crypt",
                                                        "ldap_sha512_crypt"])
    if plaintext is True:
        if password == hashed:
            return True
        else:
            return False
    else:
        if pwd_context.verify(password, hashed):
            return True
        else:
            return False
