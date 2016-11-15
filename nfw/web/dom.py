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


class Dom(object):
    def __init__(self, name=None):
        self.attributes = {}
        self.contents = []

        if name is not None:
            self.element = name
        else:
            self.element = None

        self.void_elements = ["area", "base", "br", "col",
                              "command", "embed", "hr", "img",
                              "input", "keygen", "link", "meta",
                              "param", "source", "track", "wbr"]

        self.elements = {}
        self.elements['html'] = []
        self.elements['html'].append('manifest')
        self.elements['head'] = []
        self.elements['title'] = []
        self.elements['base'] = []
        self.elements['base'].append('href')
        self.elements['base'].append('target')
        self.elements['link'] = []
        self.elements['link'].append('href')
        self.elements['link'].append('rel')
        self.elements['link'].append('media')
        self.elements['link'].append('hreflang')
        self.elements['link'].append('type')
        self.elements['link'].append('sizes')
        self.elements['meta'] = []
        self.elements['meta'].append('name')
        self.elements['meta'].append('http-equiv')
        self.elements['meta'].append('content')
        self.elements['meta'].append('charset')
        self.elements['style'] = []
        self.elements['style'].append('media')
        self.elements['style'].append('type')
        self.elements['style'].append('scoped')
        self.elements['script'] = []
        self.elements['script'].append('src')
        self.elements['script'].append('async')
        self.elements['script'].append('defer')
        self.elements['script'].append('type')
        self.elements['script'].append('charset')
        self.elements['noscript'] = []
        self.elements['body'] = []
        self.elements['body'].append('onafterprint')
        self.elements['body'].append('onbeforeprint')
        self.elements['body'].append('onbeforeunload')
        self.elements['body'].append('onblur')
        self.elements['body'].append('onerror')
        self.elements['body'].append('onfocus')
        self.elements['body'].append('onhashchange')
        self.elements['body'].append('onload')
        self.elements['body'].append('onmessage')
        self.elements['body'].append('onoffline')
        self.elements['body'].append('ononline')
        self.elements['body'].append('onpagehide')
        self.elements['body'].append('onpageshow')
        self.elements['body'].append('onpopstate')
        self.elements['body'].append('onresize')
        self.elements['body'].append('onscroll')
        self.elements['body'].append('onstorage')
        self.elements['body'].append('onunload')
        self.elements['section'] = []
        self.elements['nav'] = []
        self.elements['article'] = []
        self.elements['aside'] = []
        self.elements['h1'] = []
        self.elements['h2'] = []
        self.elements['h3'] = []
        self.elements['h4'] = []
        self.elements['h5'] = []
        self.elements['h6'] = []
        self.elements['hgroup'] = []
        self.elements['header'] = []
        self.elements['footer'] = []
        self.elements['address'] = []
        self.elements['p'] = []
        self.elements['hr'] = []
        self.elements['pre'] = []
        self.elements['blockquote'] = []
        self.elements['blockquote'].append('cite')
        self.elements['ol'] = []
        self.elements['ol'].append('reversed')
        self.elements['ol'].append('start')
        self.elements['ul'] = []
        self.elements['li'] = []
        self.elements['li'].append('value')
        self.elements['dl'] = []
        self.elements['dt'] = []
        self.elements['dd'] = []
        self.elements['figure'] = []
        self.elements['figcaption'] = []
        self.elements['div'] = []
        self.elements['a'] = []
        self.elements['a'].append('href')
        self.elements['a'].append('target')
        self.elements['a'].append('ping')
        self.elements['a'].append('rel')
        self.elements['a'].append('media')
        self.elements['a'].append('hreflang')
        self.elements['a'].append('type')
        self.elements['em'] = []
        self.elements['strong'] = []
        self.elements['small'] = []
        self.elements['s'] = []
        self.elements['cite'] = []
        self.elements['q'] = []
        self.elements['q'].append('cite')
        self.elements['dfn'] = []
        self.elements['abbr'] = []
        self.elements['data'] = []
        self.elements['data'].append('value')
        self.elements['time'] = []
        self.elements['time'].append('datetime')
        self.elements['time'].append('pubdate')
        self.elements['code'] = []
        self.elements['var'] = []
        self.elements['samp'] = []
        self.elements['kbd'] = []
        self.elements['sub'] = []
        self.elements['sup'] = []
        self.elements['i'] = []
        self.elements['b'] = []
        self.elements['u'] = []
        self.elements['mark'] = []
        self.elements['ruby'] = []
        self.elements['rt'] = []
        self.elements['rp'] = []
        self.elements['bdi'] = []
        self.elements['bdo'] = []
        self.elements['span'] = []
        self.elements['br'] = []
        self.elements['wbr'] = []
        self.elements['ins'] = []
        self.elements['ins'].append('cite')
        self.elements['ins'].append('datetime')
        self.elements['del'] = []
        self.elements['del'].append('cite')
        self.elements['del'].append('datetime')
        self.elements['img'] = []
        self.elements['img'].append('alt')
        self.elements['img'].append('src')
        self.elements['img'].append('srcset')
        self.elements['img'].append('crossorigin')
        self.elements['img'].append('usemap')
        self.elements['img'].append('ismap')
        self.elements['img'].append('width')
        self.elements['img'].append('height')
        self.elements['iframe'] = []
        self.elements['iframe'].append('src')
        self.elements['iframe'].append('srcdoc')
        self.elements['iframe'].append('name')
        self.elements['iframe'].append('sandbox')
        self.elements['iframe'].append('seamless')
        self.elements['iframe'].append('width')
        self.elements['iframe'].append('height')
        self.elements['embed'] = []
        self.elements['embed'].append('src')
        self.elements['embed'].append('type')
        self.elements['embed'].append('width')
        self.elements['embed'].append('height')
        self.elements['object'] = []
        self.elements['object'].append('data')
        self.elements['object'].append('type')
        self.elements['object'].append('typemustmatch')
        self.elements['object'].append('name')
        self.elements['object'].append('usemap')
        self.elements['object'].append('form')
        self.elements['object'].append('width')
        self.elements['object'].append('height')
        self.elements['param'] = []
        self.elements['param'].append('name')
        self.elements['param'].append('value')
        self.elements['video'] = []
        self.elements['video'].append('src')
        self.elements['video'].append('crossorigin')
        self.elements['video'].append('poster')
        self.elements['video'].append('preload')
        self.elements['video'].append('autoplay')
        self.elements['video'].append('mediagroup')
        self.elements['video'].append('loop')
        self.elements['video'].append('muted')
        self.elements['video'].append('controls')
        self.elements['video'].append('width')
        self.elements['video'].append('height')
        self.elements['audio'] = []
        self.elements['audio'].append('src')
        self.elements['audio'].append('crossorigin')
        self.elements['audio'].append('preload')
        self.elements['audio'].append('autoplay')
        self.elements['audio'].append('mediagroup')
        self.elements['audio'].append('loop')
        self.elements['audio'].append('muted')
        self.elements['audio'].append('controls')
        self.elements['source'] = []
        self.elements['source'].append('src')
        self.elements['source'].append('type')
        self.elements['source'].append('media')
        self.elements['track'] = []
        self.elements['track'].append('default')
        self.elements['track'].append('kind')
        self.elements['track'].append('label')
        self.elements['track'].append('src')
        self.elements['track'].append('srclang')
        self.elements['canvas'] = []
        self.elements['canvas'].append('width')
        self.elements['canvas'].append('height')
        self.elements['main'] = []
        self.elements['map'] = []
        self.elements['map'].append('name')
        self.elements['area'] = []
        self.elements['area'].append('alt')
        self.elements['area'].append('coords')
        self.elements['area'].append('shape')
        self.elements['area'].append('href')
        self.elements['area'].append('target')
        self.elements['area'].append('ping')
        self.elements['area'].append('rel')
        self.elements['area'].append('media')
        self.elements['area'].append('hreflang')
        self.elements['area'].append('type')
        self.elements['table'] = []
        self.elements['caption'] = []
        self.elements['colgroup'] = []
        self.elements['colgroup'].append('span')
        self.elements['col'] = []
        self.elements['col'].append('span')
        self.elements['tbody'] = []
        self.elements['thead'] = []
        self.elements['tfoot'] = []
        self.elements['tr'] = []
        self.elements['td'] = []
        self.elements['td'].append('colspan')
        self.elements['td'].append('rowspan')
        self.elements['td'].append('headers')
        self.elements['th'] = []
        self.elements['th'].append('colspan')
        self.elements['th'].append('rowspan')
        self.elements['th'].append('headers')
        self.elements['th'].append('scope')
        self.elements['th'].append('abbr')
        self.elements['form'] = []
        self.elements['form'].append('accept-charset')
        self.elements['form'].append('action')
        self.elements['form'].append('autocomplete')
        self.elements['form'].append('enctype')
        self.elements['form'].append('method')
        self.elements['form'].append('name')
        self.elements['form'].append('novalidate')
        self.elements['form'].append('target')
        self.elements['form'].append('onsubmit')
        self.elements['fieldset'] = []
        self.elements['fieldset'].append('disabled')
        self.elements['fieldset'].append('form')
        self.elements['fieldset'].append('name')
        self.elements['legend'] = []
        self.elements['label'] = []
        self.elements['label'].append('form')
        self.elements['label'].append('for')
        self.elements['input'] = []
        self.elements['input'].append('accept')
        self.elements['input'].append('alt')
        self.elements['input'].append('autocomplete')
        self.elements['input'].append('autofocus')
        self.elements['input'].append('checked')
        self.elements['input'].append('dirname')
        self.elements['input'].append('disabled')
        self.elements['input'].append('form')
        self.elements['input'].append('formaction')
        self.elements['input'].append('formenctype')
        self.elements['input'].append('formmethod')
        self.elements['input'].append('formnovalidate')
        self.elements['input'].append('formtarget')
        self.elements['input'].append('height')
        self.elements['input'].append('inputmode')
        self.elements['input'].append('list')
        self.elements['input'].append('max')
        self.elements['input'].append('maxlength')
        self.elements['input'].append('min')
        self.elements['input'].append('multiple')
        self.elements['input'].append('name')
        self.elements['input'].append('pattern')
        self.elements['input'].append('placeholder')
        self.elements['input'].append('readonly')
        self.elements['input'].append('required')
        self.elements['input'].append('size')
        self.elements['input'].append('src')
        self.elements['input'].append('step')
        self.elements['input'].append('type')
        self.elements['input'].append('value')
        self.elements['input'].append('width')
        self.elements['button'] = []
        self.elements['button'].append('autofocus')
        self.elements['button'].append('disabled')
        self.elements['button'].append('form')
        self.elements['button'].append('formaction')
        self.elements['button'].append('formenctype')
        self.elements['button'].append('formmethod')
        self.elements['button'].append('formnovalidate')
        self.elements['button'].append('formtarget')
        self.elements['button'].append('name')
        self.elements['button'].append('type')
        self.elements['button'].append('value')
        self.elements['select'] = []
        self.elements['select'].append('autofocus')
        self.elements['select'].append('disabled')
        self.elements['select'].append('form')
        self.elements['select'].append('multiple')
        self.elements['select'].append('name')
        self.elements['select'].append('required')
        self.elements['select'].append('size')
        self.elements['datalist'] = []
        self.elements['datalist'].append('option')
        self.elements['optgroup'] = []
        self.elements['optgroup'].append('disabled')
        self.elements['optgroup'].append('label')
        self.elements['option'] = []
        self.elements['option'].append('disabled')
        self.elements['option'].append('label')
        self.elements['option'].append('selected')
        self.elements['option'].append('value')
        self.elements['textarea'] = []
        self.elements['textarea'].append('autocomplete')
        self.elements['textarea'].append('autofocus')
        self.elements['textarea'].append('cols')
        self.elements['textarea'].append('dirname')
        self.elements['textarea'].append('disabled')
        self.elements['textarea'].append('form')
        self.elements['textarea'].append('inputmode')
        self.elements['textarea'].append('maxlength')
        self.elements['textarea'].append('name')
        self.elements['textarea'].append('placeholder')
        self.elements['textarea'].append('readonly')
        self.elements['textarea'].append('required')
        self.elements['textarea'].append('rows')
        self.elements['textarea'].append('wrap')
        self.elements['keygen'] = []
        self.elements['keygen'].append('autofocus')
        self.elements['keygen'].append('challenge')
        self.elements['keygen'].append('disabled')
        self.elements['keygen'].append('form')
        self.elements['keygen'].append('keytype')
        self.elements['keygen'].append('name')
        self.elements['output'] = []
        self.elements['output'].append('for')
        self.elements['output'].append('form')
        self.elements['output'].append('name')
        self.elements['progress'] = []
        self.elements['progress'].append('value')
        self.elements['progress'].append('max')
        self.elements['meter'] = []
        self.elements['meter'].append('value')
        self.elements['meter'].append('min')
        self.elements['meter'].append('max')
        self.elements['meter'].append('low')
        self.elements['meter'].append('high')
        self.elements['meter'].append('optimum')
        self.elements['details'] = []
        self.elements['details'].append('open')
        self.elements['summary'] = []
        self.elements['command'] = []
        self.elements['command'].append('type')
        self.elements['command'].append('label')
        self.elements['command'].append('icon')
        self.elements['command'].append('disabled')
        self.elements['command'].append('checked')
        self.elements['command'].append('radiogroup')
        self.elements['command'].append('command')
        self.elements['menu'] = []
        self.elements['menu'].append('type')
        self.elements['menu'].append('label')
        self.elements['dialog'] = []
        self.elements['dialog'].append('open')
        self.elements['global'] = []
        self.elements['global'].append('accesskey')
        self.elements['global'].append('class')
        self.elements['global'].append('contenteditable')
        self.elements['global'].append('contextmenu')
        self.elements['global'].append('dir')
        self.elements['global'].append('draggable')
        self.elements['global'].append('dropzone')
        self.elements['global'].append('hidden')
        self.elements['global'].append('id')
        self.elements['global'].append('inert')
        self.elements['global'].append('itemid')
        self.elements['global'].append('itemprop')
        self.elements['global'].append('itemref')
        self.elements['global'].append('itemscope')
        self.elements['global'].append('itemtype')
        self.elements['global'].append('lang')
        self.elements['global'].append('role')
        self.elements['global'].append('spellcheck')
        self.elements['global'].append('style')
        self.elements['global'].append('tabindex')
        self.elements['global'].append('title')
        self.elements['global'].append('translate')
        self.elements['global'].append('onclick')
        self.elements['global'].append('onchange')
        self.elements['global'].append('name')

        self.input_types = ["hidden", "text", "search", "tel",
                            "url", "email", "password", "datetime",
                            "date", "month", "week", "time",
                            "datetime-local", "number", "range",
                            "color", "checkbox", "radio", "file",
                            "submit", "image", "reset", "button"]

    def create_element(self, name):
        name = name.lower()
        if name in self.elements:
            element = Dom(name)
            self.contents.append(element)
            return element
        else:
            raise Exception("DOM: No such tag/element %s" % (name,) +
                            " in HTML5")

    def set_attribute(self, attribute, value=None):
        attribute = attribute.lower()
        if self.element is not None:
            if self.element == 'input':
                if attribute == 'type':
                    value = value.lower()
                    if value not in self.input_types:
                        raise Exception("DOM: Setting unknown" +
                                        " input type on %s" %
                                        (self.element,))
            if attribute in self.elements[self.element]:
                self.attributes[attribute] = value
            else:
                if attribute in self.elements['global']:
                    self.attributes[attribute] = value
                elif len(attribute) > 5 and attribute[0:5] == 'aria-':
                    self.attributes[attribute] = value
                elif len(attribute) > 5 and attribute[0:5] == 'data-':
                    self.attributes[attribute] = value
                else:
                    raise Exception("DOM: Setting unknown" +
                                    " attribute %s on %s" %
                                    (attribute, self. element))
        else:
            raise Exception("DOM: Setting attribute" +
                            " %s on root" % (attribute,))

    def append(self, value):
        if self.element in self.void_elements:
            raise Excption("DOM: Appending on void" +
                           " element %s" % (self.element,))
        else:
            self.contents.append(value)

    def prepend(self, value):
        if self.element in self.void_elements:
            raise Exception("DOM: Prepending on void" +
                            " element %s" % (self.element,))
        else:
            self.contents[:0] = value

    def get_contents(self):
        to_return = None
        for content in self.contents:
            if content is not None:
                if isinstance(content, nfw.web.Dom):
                    if to_return is not None:
                        to_return = "%s%s" % (to_return, content.get())
                    else:
                        to_return = "%s" % (content.get())
                else:
                    if to_return is not None:
                        to_return = "%s%s" % (to_return, content)
                    else:
                        to_return = "%s" % (content)

        return to_return

    def get(self):
        to_return = None
        attributes = None
        for attribute in self.attributes:
            value = self.attributes[attribute]
            if value is not None:
                if isinstance(value, str) or isinstance(value, unicode):
                    value = value.replace("\"", "\\\"")
                if value != '':
                    if attributes is not None:
                        attributes = "%s %s=\"%s\"" % (attributes,
                                                       attribute, value)
                    else:
                        attributes = " %s=\"%s\"" % (attribute, value)
                else:
                    if attributes is not None:
                        attributes = "%s %s" % (attributes, attribute)
                    else:
                        attributes = " %s" % (attribute)
            else:
                if attributes is not None:
                    attributes = "%s %s" % (attributes, attribute)
                else:
                    attributes = " %s" % (attribute)

        if self.element is not None:
            if attributes is not None:
                to_return = "<%s%s>" % (self.element, attributes)
            else:
                to_return = "<%s>" % (self.element)

        if len(self.contents) > 0:
            contents = self.get_contents()
            if contents is not None:
                if to_return is None:
                    to_return = "%s" % (contents)
                else:
                    to_return = "%s%s" % (to_return, contents)
        if self.element is not None:
            if self.element not in self.void_elements:
                if (len(self.contents) > 1):
                    to_return = "%s" % (to_return,)
                if self.element is not None:
                    to_return = "%s</%s>" % (to_return, self.element)
                else:
                    to_return = "%s</%s>" % (self.element,)

        return to_return
