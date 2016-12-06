# Neutrino Framework
#
# Copyright (c) 2015-2016, Christiaan Frans Rademan
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

import nfw

class Menu(object):
    def __init__(self):
        self.dom = nfw.web.Dom()

    def add_divider(self):
        li = self.dom.create_element('li')
        li.set_attribute('role','seperator')
        li.set_attribute('class','divider')

    def add_dropdown_heading(self, name):
        li = self.dom.create_element('li')
        li.set_attribute('class','dropdown-header')
        li.append(name)

    def add_submenu(self, name, menu):
        li = self.dom.create_element('li')
        li.set_attribute('class','dropdown-submenu')
        a = li.create_element('a')
        a.set_attribute('href','#')
        a.set_attribute('class','dropdown-toggle')
        a.set_attribute('data-toggle','dropdown')
        a.append(name)
        ul = li.create_element('ul')
        ul.set_attribute('class','dropdown-menu')
        ul.append(menu)

    def add_dropdown(self, name, menu):
        li = self.dom.create_element('li')
        a = li.create_element('a')
        a.set_attribute('href','#')
        a.set_attribute('class','dropdown-toggle')
        a.set_attribute('data-toggle','dropdown')
        a.append(name)
        s = a.create_element('span')
        s.set_attribute('class','caret')
        ul = li.create_element('ul')
        ul.set_attribute('class','dropdown-menu')
        ul.append(menu)

    def add_link(self, name, url, active=False, target=None, modal_target=None):
        li = self.dom.create_element('li')
        if active is True:
            li.set_attribute('class','nav-link active')
        else:
            li.set_attribute('class','nav-link')
        a = li.create_element('a')
        if target is not None:
            a.set_attribute('target',target)
        if modal_target is not None:
            a.set_attribute('data-show','true')
            a.set_attribute('data-toggle','modal')
            a.set_attribute('data-target',modal_target)
            a.set_attribute('data-remote',url)
        a.set_attribute('href',url)
        a.append(name)

    def __str__(self):
        toreturn = self.dom.get()
        if toreturn is not None:
            return toreturn
        else:
            return ''
