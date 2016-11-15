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
from collections import OrderedDict
from collections import Iterator
from copy import copy
from copy import deepcopy
from datetime import datetime
import json
import uuid

import nfw
from nfw.utils import ObjectName

log = logging.getLogger(__name__)


def _declared_fields(cls):
    current_fields = []
    for name in dir(cls):
        prop = getattr(cls, name)
        if isinstance(prop, Field):
            prop = deepcopy(prop)
            current_fields.append((name, prop))
            prop._name = name

    current_fields.sort(key=lambda x: x[1].creation_counter)
    return OrderedDict(current_fields)


class FieldChecks(object):
    def validate_length(self, value):
        if (self.max_length is not None and
                self.max_length != 0 and
                len(value) > self.max_length):
            raise nfw.ModelFieldError(self._name,
                                      self.label,
                                      'exceeded maximum length',
                                      self.max_length)

        if len(value) < self.min_length:
            raise nfw.ModelFieldError(self._name,
                                      self.label,
                                      'less than required length',
                                      self.min_length)

    def size(self, value):
        if (self.maximum is not None and
                value > self.maximum):
            raise nfw.ModelFieldError(self._name,
                                      self.label,
                                      'exceeded maximum value',
                                      self.maximum)

        if (self.minimum is not None and
                value < self.minimum):
            raise nfw.ModelFieldError(self._name,
                                      self.label,
                                      'less than minimum value',
                                      self.minimum)

    def is_string(self, value):
        if not isinstance(value, basestring):
            raise nfw.ModelFieldError(self._name,
                                      self.label,
                                      'invalid string value',
                                      value)

    def is_integer(self, value):
        if not isinstance(value, (int, long)):
            raise nfw.ModelFieldError(self._name,
                                      self.label,
                                      'invalid integer value',
                                      value)

    def is_number(self, value):
        if not isinstance(value, (int, long, float)):
            raise nfw.ModelFieldError(self._name,
                                      self.label,
                                      'invalid number value',
                                      value)

    def is_bool(self, value):
        if not isinstance(value, (int, long, float, bool)):
            raise nfw.ModelFieldError(self._name,
                                      self.label,
                                      'invalid boolean value',
                                      value)


class Mysql(object):
    def __init__(self, db, model_name, meta, declared_fields):
        self.db = db
        self.declared_fields = declared_fields

        if hasattr(meta, 'db_table'):
            self.db_table = meta.db_table
        else:
            self.db_table = model_name

        if hasattr(meta, 'db_primary_key'):
            self.db_primary_key = meta.db_primary_key
        else:
            self.db_primary_key = 'id'

        if hasattr(meta, 'db_query'):
            self.db_query = meta.db_query
        else:
            fields = ", ".join(self.declared_fields)
            self.db_query = "SELECT %s FROM %s" % (fields, self.db_table,)

    def foreign_key(self, id=None, key=None):
        fields = ", ".join(self.declared_fields)
        sql = "SELECT %s FROM %s" % (fields, self.db_table,)
        sql += " WHERE %s = %s" % (key, '%s')
        result = self.db.execute(sql, (id,))
        if len(result) > 0:
            if len(result) == 1:
                return result[0][self.db_primary_key]
            else:
                raise MultipleObjectsReturned("Multiple rows for foreign key")

    def select(self, id=None, field=None, sql=None):
        if sql is None:
            sql = self.db_query

        result = None
        if id is not None:
            fields = ", ".join(self.declared_fields)
            sql = "SELECT %s FROM %s" % (fields, self.db_table,)
            sql += " WHERE %s = %s" % (self.db_primary_key, '%s')
            result = self.db.execute(sql, (id,))
            if len(result) > 0:
                if len(result) != 1:
                    raise nfw.MultipleObjectsReturned("Multiple rows for id")
            else:
                raise nfw.DoesNotExist("No row matching id")
        else:
            result = self.db.execute(sql)
        return self._clean(result)

    def _clean(self, result):
        clean = []
        for r in result:
            t = {}
            for f in r:
                if f in self.declared_fields:
                    t[f] = r[f]
            clean.append(t)
        return clean

    def insert(self, data):
        fields = []
        values = []

        insert = []
        sql_str_values = []
        for field in data:
            fields.append(field)
            values.append(data[field])
            insert.append("%s" % (field))
            sql_str_values.append("%s" % ('%s'))

        insert = ",".join(insert)
        sql_str_values = ",".join(sql_str_values)
        new_id = uuid.uuid4()

        sql = "INSERT INTO %s (%s)" % (self.db_table, insert) +\
              " VALUES (%s)" % (sql_str_values,)
        self.db.execute(sql, tuple(values))

        return self.db.last_row_id()

    def update(self, data, id):
        fields = []
        values = []
        update = []
        sql_str_values = []
        for field in data:
            fields.append(field)
            values.append(data[field])
            update.append("%s=%s" % (field, "%s"))
        values.append(id)

        update = ",".join(update)

        sql = "UPDATE %s SET %s" % (self.db_table, update) +\
              " WHERE %s = %s" % (self.db_primary_key, '%s')
        self.db.execute(sql, tuple(values))

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def delete(self, id):
        sql = "DELETE FROM %s WHERE %s = %s" % (self.db_table,
                                                self.db_primary_key,
                                                '%s')
        self.db.execute(sql, (id,))


class Field(ObjectName):
    def __init__(self, value=None, pri_id=None, db=None, **kwargs):
        self.creation_counter = nfw.creation_counter()
        self._declared_fields = _declared_fields(self)
        self._id = pri_id
        self._name = None
        self._data = None
        self._model = self.__class__.__name__
        self._table = self._model
        self._dbo = db
        self._updated = False

        self._parent = None
        self._parent_key = None
        self._parent_key_value = None

        if hasattr(self, '_init'):
            self._init()
        if hasattr(self, '_validate'):
            self._validate(value)
        if hasattr(self, '_set'):
            self._set(value)

        attributes = {
                'label': self._name,
                'rows': 1,
                'length': None,
                'cols': None,
                'hidden': False,
                'readonly': False,
                'placeholder': None,
                'prefix': None,
                'suffix': None,
                'foreign_key': None,
                'required': False,
                'choices': None,
                'null': False,
                'max_length': None,
                'min_length': 0
                }

        if hasattr(self, '_attributes'):
            attributes.update(self._attributes)
        self._attributes = attributes

        for arg in kwargs:
            if arg in self._attributes:
                self._attributes[arg] = kwargs[arg]

        for attr in self._attributes:
            setattr(self, attr,  self._attributes[attr])

        self._init_db()

    class Meta(object):
        pass

    def _init_db(self):
        if self._dbo is not None:
            self._db = Mysql(self._dbo,
                             self._table,
                             self.Meta,
                             self._declared_fields)
            if hasattr(self.Meta, 'db_primary_key'):
                self._db_primary_key = self.Meta.db_primary_key
            else:
                self._db_primary_key = 'id'

    def _val(self, value):
        if hasattr(self, '_validate'):
            value = self._validate(value)
        return value

    def _get_field(self, field):
        if field in self._declared_fields:
            field = deepcopy(self._declared_fields[field])
            return field
        else:
            raise nfw.FieldDoesNotExist(field)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __contains__(self, key):
        return key in self._data

    def value(self):
        return self._data

    class _JsonEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o.value(), datetime):
                return str(o.value().strftime("%Y/%m/%d %H:%M:%S"))
            else:
                return o.value()

    class _JsonDecoder(json.JSONDecoder):
        def __init__(self, list_type=list,  **kwargs):
            json.JSONDecoder.__init__(self, **kwargs)
            # Use the custom JSONArray
            self.parse_array = self.JSONArray
            # Use the python implemenation of the scanner
            self.scan_once = json.scanner.py_make_scanner(self)
            self.list_type = list_type

        def JSONArray(self, s_and_end, scan_once, **kwargs):
            values, end = json.decoder.JSONArray(s_and_end,
                                                 scan_once,
                                                 **kwargs)
            return self.list_type(values), end

    def dump_json(self, **kwargs):
        return json.dumps(self,
                          cls=self._JsonEncoder,
                          **kwargs)

    def load_json(self, fp, **kwargs):
        json.loads(fp, cls=self._JsonDecoder, list_type=self)

    def commit(self):
        if hasattr(self, '_db'):
            if self._updated is True:
                self._db.commit()
                self._updated = False

    def rollback(self):
        if hasattr(self, '_db'):
            self._db.rollback()


class Fields(object):
    class List(Field):
        def _init(self):
            self._data = []

        def __setitem__(self, key, value):
            self._data[key]._set(value)

        def __getitem__(self, key):
            return self._data[key]

        def __delitem__(self, key):
            if hasattr(self._data[key], '__del__'):
                self._data[key].__del__()
            del self._data[key]

        def __iter__(self):
            return iter(self._data)

        def append(self, v, _load=False):
            new = Fields.Dict()
            setattr(new, '_declared_fields', self._declared_fields)
            if hasattr(self, 'Meta'):
                new._table = self._table
                new.Meta = self.Meta
                new._init_db()
            new._set(v, _load)
            self._data.append(new)

        def query(self, sql=None):
            if hasattr(self, '_db'):
                self._data = []
                result = self._db.select(sql=sql)
                for row in result:
                    self.append(row, True)

        def __call__(self, v):
            for i in v:
                self.append(i)

    class Dict(Field):
        def _init(self):
            self._data = {}

        def _set(self, v, _load=False):
            if v is not None:
                if isinstance(v, dict):
                    updates = {}
                    for i in v:
                        val = v[i]
                        if i not in self._data:
                            self._data[i] = self._get_field(i)
                            if isinstance(self._data[i], Fields.List):
                                raise nfw.ValidationError("Property is a" +
                                                          " List Model")
                            else:
                                val = self._data[i]._val(val)
                        else:
                            if hasattr(self, '_db_primary_key') and i == self._db_primary_key:
                                raise nfw.ValidationError("Cannot set" +
                                                          " primary key")
                        if isinstance(self._data[i], Fields.Dict):
                            self._data[i]._parent = self
                            self._data[i]._parent_key = i
                            if isinstance(val, dict):
                                self._data[i](val)
                                fk = self._data[i].foreign_key
                                if fk in val:
                                    updates[i] = val[fk]
                            else:
                                self._data[i]._parent_key_value = val
                                self._data[i].query()
                                updates[i] = val
                        else:
                            updates[i] = val
                            if hasattr(self._data[i],'_validate'):
                                val = self._data[i]._validate(val)
                            self._data[i]._set(val)
                    if hasattr(self, '_db') and _load is False:
                        if len(updates) > 0:
                            self._updated = True
                            if self._db_primary_key in self._data:
                                pri_id = self._data[self._db_primary_key]
                                if len(self._db.select(id=pri_id)) > 0:
                                        self._db.update(updates, pri_id)
                                else:
                                    pri_id = self._db.insert(updates)
                                    updates[self._db_primary_key] = pri_id
                                    if self.foreign_key in updates:
                                        self._parent_key_value = updates[self.foreign_key]
                                        self._parent._set({self._parent_key: self._parent_key_value})
                                        self._data[self._db_primary_key] = pri_id
                            else:
                                self._data[self._db_primary_key] = self._get_field(self._db_primary_key)
                                pri_id = self._db.insert(updates)
                                updates[self._db_primary_key] = pri_id
                                self._data[self._db_primary_key]._set(pri_id)
                                self._id = pri_id
                                if self.foreign_key in updates:
                                    self._parent_key_value = updates[self.foreign_key]
                                    self._parent._set({self._parent_key: self._parent_key_value})
                else:
                    raise nfw.ValidationError("'%s' Expecting dictionary" % (str(self._objectname()),))

        def __setitem__(self, key, value):
            self._set({key: value})

        def __getitem__(self, key):
            if hasattr(self, key):
                if key in self._data:
                    return self._data[key]
                else:
                    self._data[key] = self._get_field(key)
                    if isinstance(self._data[key], nfw.Model.Bool):
                        self._data[key]._set(False)
                    return self._data[key]
            else:
                return self._data[key]

        def __delitem__(self, key):
            if hasattr(self._data[key], '__del__'):
                self._data[key].__del__()
            else:
                del self._data[key]

        def __del__(self):
            self._data = {}

        def delete(self):
            if self.foreign_key is None:
                if self._db_primary_key in self._data:
                    pri_id = self._data[self._db_primary_key]
                    self._db.delete(pri_id)
            else:
                if self._parent_key in self._parent:
                    self._parent[self._parent_key] = None
            self._data = {}

        def __iter__(self):
            results = OrderedDict()
            for key in self._declared_fields:
                if key in self._data:
                    results[key] = self._data[key]
            return iter(results)

        def value(self):
            results = OrderedDict()
            for key in self._declared_fields:
                if key in self._data:
                    results[key] = self._data[key]
            return results

        def query(self, sql=None):
            if hasattr(self, '_db'):
                if self.foreign_key is not None:
                    if self._parent_key_value is not None:
                        self._id = self._db.foreign_key(self._parent_key_value, self.foreign_key)
                self._data = {}
                if self._id is not None:
                    result = self._db.select(id=self._id, sql=sql)
                    if len(result) == 1:
                        self._set(result[0], True)

        def get(self, key, default=None):
            try:
                return self._data[key]
            except KeyError:
                return default

        def __call__(self, v):
            self._set(v)

    class Integer(Field, FieldChecks):
        _attributes = {
                'minimum': None,
                'maximum': None
                }

        def _init(self):
            self._data = None

        def _set(self, value):
            self._data = value

        def _validate(self, value):
            if value is not None:
                self.is_integer(value)
                self.size(value)
            return value

    class Number(Field, FieldChecks):
        _attributes = {
                'minimum': None,
                'maximum': None
                }

        def _init(self):
            self._data = None

        def _set(self, value):
            self._data = value

        def _validate(self, value):
            if value is not None:
                self.is_number(value)
                self.size(value)
            return value

    class Bool(Field, FieldChecks):
        _attributes = {
                }

        def _init(self):
            self._data = None

        def _set(self, value):
            self._data = value

        def _validate(self, value):
            if value is not None:
                self.is_bool(value)
            else:
                value = False
            if value == 1:
                value = True
            if value is True:
                return True
            else:
                return False

    class Text(Field, FieldChecks):
        _attributes = {
                }

        def _init(self):
            self._data = None

        def _set(self, value):
            self._data = value

        def _validate(self, value):
            if value is not None:
                self.is_string(value)
                self.validate_length(value)
            return value


class Model(Fields, Fields.List):
    pass


class ModelDict(Fields, Fields.Dict):
    pass
