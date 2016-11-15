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
from .. import forms

class Form(forms.Base):
    def checkbox(self, name, value, label, readonly=False, prefix=None, suffix=None):
        dom = nfw.web.Dom()
        form_group = dom.create_element('div')
        form_group.set_attribute('class', 'form-group')
        col_sm = form_group.create_element('div')
        col_sm.set_attribute('class', 'col-sm-offset-3 col-sm-9')
        checkbox = col_sm.create_element('div')
        checkbox.set_attribute('class', 'checkbox')

        l = checkbox.create_element('label')
        l.set_attribute('for', name)

        f = l.create_element('input')
        f.set_attribute('type', 'checkbox')
        f.set_attribute('id', name)
        f.set_attribute('name', name)

        if value is True:
            f.set_attribute('checked')

        l.append(label)

        return dom

    def select(self, name, value, options, label=None, readonly=False, prefix=None, suffix=None):
        dom = nfw.web.Dom()
        form_group = dom.create_element('div')
        form_group.set_attribute('class', 'form-group')

        l = form_group.create_element('label')
        l.set_attribute('for', name)
        l.set_attribute('class', 'control-label col-sm-3')
        l.append(label)

        field = form_group.create_element('div')
        field.set_attribute('class', 'input-group col-sm-9')

        if prefix is not None:
            p = field.create_element('span')
            p.set_attribute('class', 'input-group-addon')
            p.append(prefix)

        f = field.create_element('select')
        f.set_attribute('id', name)
        f.set_attribute('name', name)
        f.set_attribute('class', 'form-control')
        for o in options:
            option = f.create_element('option')
            option.set_attribute('value', o)

            if o == value:
                option.set_attribute('selected')

            if readonly is True:
                f.set_attribute('disabled', 'disabled')

            option.append(options[o])

        if suffix is not None:
            s = field.create_element('span')
            s.set_attribute('class', 'input-group-addon')
            s.append(suffix)

        return dom

    def input(self, name, value, label=None, readonly=False, prefix=None, suffix=None, required=False, size=None, max_length=None, placeholder=None):
        dom = nfw.web.Dom()
        form_group = dom.create_element('div')
        form_group.set_attribute('class', 'form-group')

        l = form_group.create_element('label')
        l.set_attribute('for', name)
        l.set_attribute('class', 'control-label col-sm-3')
        l.append(label)

        field = form_group.create_element('div')
        field.set_attribute('class', 'input-group col-sm-9')

        if prefix is not None:
            p = field.create_element('span')
            p.set_attribute('class', 'input-group-addon')
            p.append(prefix)

        f = field.create_element('input')
        f.set_attribute('id', name)
        f.set_attribute('name', name)
        f.set_attribute('type', 'text')
        f.set_attribute('value', value)
        f.set_attribute('class', 'form-control')

        if required is True:
            f.set_attribute('required')

        if readonly is True:
            f.set_attribute('readonly')

        if placeholder is not None:
            f.set_attribute('placeholder',placeholder)

        if max_length is not None:
            f.set_attribute('maxlength', max_length)

        if size is not None:
            f.set_attribute('size', size)

        if suffix is not None:
            s = field.create_element('span')
            s.set_attribute('class', 'input-group-addon')
            s.append(suffix)

        return dom

    def textarea(self, name, value, label=None, readonly=False, prefix=None, suffix=None, required=False, rows=None, cols=None, placeholder=None):
        dom = nfw.web.Dom()

        form_group = dom.create_element('div')
        form_group.set_attribute('class', 'form-group')

        l = form_group.create_element('label')
        l.set_attribute('for', name)
        l.set_attribute('class', 'control-label col-sm-3')
        l.append(label)

        field = form_group.create_element('div')
        field.set_attribute('class', 'input-group col-sm-9')

        if prefix is not None:
            p = field.create_element('span')
            p.set_attribute('class', 'input-group-addon')
            p.append(prefix)

        f = field.create_element('textarea')
        f.set_attribute('id', name)
        f.set_attribute('name', name)
        f.set_attribute('class', 'form-control')
        f.append(value)

        if required is True:
            f.set_attribute('required')

        if readonly is True:
            f.set_attribute('readonly')

        if placeholder is not None:
            f.set_attribute('placeholder',placeholder)

        if cols is not None:
            f.set_attribute('cols', cols)

        if rows is not None:
            f.set_attribute('rows', rows)

        if suffix is not None:
            s = field.create_element('span')
            s.set_attribute('class', 'input-group-addon')
            s.append(suffix)

        return dom
