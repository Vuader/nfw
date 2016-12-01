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
import ConfigParser
import logging

import nfw

log = logging.getLogger(__name__)

nfw_config = None


class Config(object):
    configs = {}

    def __init__(self, config_file=None):
        self.config = {}
        if config_file is None:
            config_file = nfw_config

        if config_file is not None:
            if os.path.isfile(config_file):
                if config_file not in self.configs:
                    config = ConfigParser.ConfigParser()
                    config.read(config_file)
                    sections = config.sections()
                    for s in sections:
                        self.config[s] = {}
                        options = config.options(s)
                        for o in options:
                            self.config[s][o] = config.get(s, o)
                    self.configs[config_file] = self.config
                else:
                    self.config = self.configs[config_file]
            else:
                raise nfw.Error("Configuration file not found: %s"
                                % (config_file,))


    def get(self, k=None, d=None):
        if k in self.config:
            return self.config[k]
        else:
            return d

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config

    def __iter__(self):
        return iter(self.config)

    def __len__(self):
        return len(self.config)
