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


class Base(nfw.ModelDict):
    def __init__(self, request=None, **kwargs):
        super(nfw.ModelDict, self).__init__(**kwargs)

        if isinstance(request, nfw.Request):
            values = request.post
            for v in values:
                if hasattr(self, v):
                    field = getattr(self, v)
                    if field.readonly is False:
                        if isinstance(field, nfw.ModelDict.Bool):
                            self._set({v: True})
                        elif isinstance(field, nfw.ModelDict.Integer):
                            try:
                                self._set({v: long(values[v].value)})
                            except:
                                self._set({v: values[v].value})
                        elif isinstance(field, nfw.ModelDict.Number):
                            try:
                                self._set({v: float(values[v].value)})
                            except:
                                self._set({v: values[v].value})
                        else:
                            self._set({v: values[v].value})

    def __str__(self):
        dom = nfw.web.Dom()
        for key in self._declared_fields:
            if key in self._data:
                value = self._data[key].value()
            else:
                value = ""

            f = self._declared_fields[key]

            if f.hidden is True:
                pass
            elif isinstance(f, nfw.ModelDict.Dict):
                pass
            elif isinstance(f, nfw.ModelDict.List):
                pass
            elif isinstance(f, nfw.ModelDict.Bool):
                dom.append(self.checkbox(key,
                                         value,
                                         label=f.label,
                                         readonly=f.readonly,
                                         prefix=f.prefix,
                                         suffix=f.suffix))
            else:
                if f.choices is not None:
                    choices = {}
                    if isinstance(f.choices, list):
                        for c in f.choices:
                            choices[c] = c
                    else:
                        choices = f.choices

                    dom.append(self.select(key,
                                           value,
                                           label=f.label,
                                           options=choices,
                                           readonly=f.readonly,
                                           prefix=f.prefix,
                                           suffix=f.suffix))
                elif f.rows > 1:
                    dom.append(self.textarea(key,
                                             value,
                                             label=f.label,
                                             readonly=f.readonly,
                                             required=f.required,
                                             cols=f.cols,
                                             rows=f.rows,
                                             placeholder=f.placeholder,
                                             prefix=f.prefix,
                                             suffix=f.suffix))
                else:
                    dom.append(self.input(key,
                                          value,
                                          label=f.label,
                                          readonly=f.readonly,
                                          required=f.required,
                                          size=f.size,
                                          max_length=f.max_length,
                                          placeholder=f.placeholder,
                                          prefix=f.prefix,
                                          suffix=f.suffix))
        return dom.get()


class Form(Base):
    def checkbox(self, name, value, label=None, readonly=False, prefix=None, suffix=None):
        dom = nfw.web.Dom()

        if label is not None:
            l = dom.create_element('label')
            l.set_attribute('for', name)
            l.append(label)

        if prefix is not None:
            dom.append(prefix)

        f = dom.create_element('input')
        f.set_attribute('type', 'checkbox')
        f.set_attribute('id', name)
        f.set_attribute('name', name)

        if value is True:
            f.set_attribute('checked')

        if suffix is not None:
            dom.append(suffix)

        return dom

    def select(self, name, value, options, label=None, readonly=False, prefix=None, suffix=None):
        dom = nfw.web.Dom()

        if label is not None:
            l = dom.create_element('label')
            l.set_attribute('for', name)
            l.append(label)

        if prefix is not None:
            dom.append(prefix)

        f = dom.create_element('select')
        f.set_attribute('id', name)
        f.set_attribute('name', name)
        for o in options:
            option = f.create_element('option')
            option.set_attribute('value', o)

            if o == value:
                option.set_attribute('selected')

            if readonly is True:
                f.set_attribute('disabled', 'disabled')

            option.append(options[o])

        if suffix is not None:
            dom.append(suffix)

        return dom

    def input(self, name, value, label=None, readonly=False, prefix=None, suffix=None, required=False, size=None, max_length=None, placeholder=None):
        dom = nfw.web.Dom()

        if label is not None:
            l = dom.create_element('label')
            l.set_attribute('for', name)
            l.append(label)

        if prefix is not None:
            dom.append(prefix)

        f = dom.create_element('input')
        f.set_attribute('id', name)
        f.set_attribute('name', name)
        f.set_attribute('type', 'text')
        f.set_attribute('value', value)

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
            dom.append(suffix)

        return dom

    def textarea(self, name, value, label=None, readonly=False, prefix=None, suffix=None, required=False, rows=None, cols=None, placeholder=None):
        dom = nfw.web.Dom()

        if label is not None:
            l = dom.create_element('label')
            l.set_attribute('for', name)
            l.append(label)

        if prefix is not None:
            dom.append(prefix)

        f = dom.create_element('textarea')
        f.set_attribute('id', name)
        f.set_attribute('name', name)
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
            dom.append(suffix)

        return dom
