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

class Model(unittest.TestCase):
    def __init__(self, methodName):
        super(Model, self).__init__(methodName)

    def test_modeldict(self):
        queries = []

        # DICT MODEL: QUERY DATABASE FOR RECORDS
        q = {}
        q['query'] = "SELECT firstname, lastname, id FROM Model WHERE id = %s"
        q['values'] = [1,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 1
        testrow['firstname'] = 'John'
        testrow['lastname'] = 'Doe'
        q['result'] = testtable
        queries.append(q)

        # GET DATABASE INTERFACE
        db = nfw.mysql.Testing(queries)

        # DICT MODEL
        class ModelDict(nfw.ModelDict):
            class Meta:
                db_table = 'Model'

            firstname = nfw.Model.Text(required=True)
            lastname = nfw.Model.Text(required=True)

        # CREATE DICT DATA MODEL
        modeldict = ModelDict(db=db, id=1)

        # DICT MODEL: QUERY DATABASE FOR RECORDS
        modeldict.query()

        db.commit()


    def test_modellist(self):
        queries = []

        # LIST MODEL: QUERY DATABASE FOR RECORDS
        q = {}
        q['query'] = "SELECT firstname, lastname, submodel FROM Model"
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 1
        testrow['firstname'] = 'John'
        testrow['lastname'] = 'Doe'
        testrow['submodel'] = 22
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "SELECT age, id FROM SubModel WHERE id = %s"
        q['values'] = [22,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 22
        testrow['age'] = 33
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "SELECT age, id FROM SubModel WHERE id = %s"
        q['values'] = [22,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 22
        testrow['age'] = 33
        q['result'] = testtable
        queries.append(q)

        # LIST MODEL: INSERT NEW RECORD
        q = {}
        q['query'] = "INSERT INTO Model (firstname,lastname) VALUES (%s,%s)"
        q['values'] = ['Jane','Doe']
        q['last_row_id'] = 1
        q['result'] = testtable
        queries.append(q)

        # LIST MODEL: DELETE RECORD
        q = {}
        q['query'] = "DELETE FROM Model WHERE id = %s"
        q['values'] = [1,]
        queries.append(q)

        # LIST MODEL: INSERT NEW RECORD
        q = {}
        q['query'] = "INSERT INTO SubModel (age) VALUES (%s)"
        q['last_row_id'] = 43
        q['values'] = [43,]
        queries.append(q)

        q = {}
        q['query'] = "SELECT age, id FROM SubModel WHERE id = %s"
        q['values'] = [43,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 43
        testrow['age'] = 43
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "SELECT age, id FROM SubModel WHERE id = %s"
        q['values'] = [43,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 43
        testrow['age'] = 43
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "INSERT INTO Model (submodel) VALUES (%s)"
        q['values'] = [43,]
        q['last_row_id'] = 3
        queries.append(q)

        q = {}
        q['query'] = "SELECT firstname, lastname, submodel, id FROM Model WHERE id = %s"
        q['values'] = [3,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 3
        testrow['submodel'] = 43
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "UPDATE Model SET firstname=%s,lastname=%s WHERE id = %s"
        q['values'] = ['Mark','Shuttleworth', 3]
        queries.append(q)

        # LIST MODEL: ALTER SUB MODEL
        q = {}
        q['query'] = "SELECT age, id FROM SubModel WHERE id = %s"
        q['values'] = [43,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 43
        testrow['age'] = 43
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "SELECT age, id FROM SubModel WHERE id = %s"
        q['values'] = [43,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 43
        testrow['age'] = 43
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "SELECT firstname, lastname, submodel, id FROM Model WHERE id = %s"
        q['values'] = [1,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 1
        testrow['firstname'] = 'Jane'
        testrow['lastname'] = 'Doe'
        testrow['submodel'] = 43
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "UPDATE Model SET submodel=%s WHERE id = %s"
        q['values'] = [43,1]
        queries.append(q)

        # LIST MODEL: DELETE SUB MODEL
        q = {}
        q['query'] = "UPDATE Model SET submodel=%s WHERE id = %s"
        q['values'] = [None,1]
        queries.append(q)

        # LIST MODEL: DELETE FIELD
        q = {}
        q['query'] = "UPDATE Model SET firstname=%s WHERE id = %s"
        q['values'] = [None,1]
        queries.append(q)

        # LIST MODEL: UPDATE FIELD
        q = {}
        q['query'] = "SELECT firstname, lastname, submodel, id FROM Model WHERE id = %s"
        q['values'] = [1,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 1
        testrow['lastname'] = 'Doe'
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "UPDATE Model SET firstname=%s WHERE id = %s"
        q['values'] = ['Bean',1]
        queries.append(q)

        # LIST MODEL: UPDATE SUB MODEL
        q = {}
        q['query'] = "SELECT age, id FROM SubModel WHERE id = %s"
        q['values'] = [43,]
        testtable = []
        testrow = {}
        testtable.append(testrow)
        testrow['id'] = 43
        testrow['age'] = 43
        q['result'] = testtable
        queries.append(q)

        q = {}
        q['query'] = "UPDATE SubModel SET age=%s WHERE id = %s"
        q['values'] = [83,43]
        queries.append(q)


        # GET DATABASE INTERFACE
        db = nfw.mysql.Testing(queries)

        # MODELS
        class SubModel(nfw.ModelDict):
            age = nfw.Model.Integer(required=True)

        class Model(nfw.Model):
            firstname = nfw.Model.Text(required=True)
            lastname = nfw.Model.Text(required=True)
            submodel = SubModel(db=db, foreign_key='id')

        # CREATE LIST DATA MODEL
        model = Model(db=db)


        # LIST MODEL: QUERY DATABASE FOR RECORDS
        model.query()

        # LIST MODEL: INSERT NEW RECORD
        model.append({'firstname':'Jane','lastname': 'Doe'})

        # LIST MODEL: DELETE RECORD
        del(model[0])

        # LIST MODEL: INSERT NEW RECORD
        model.append({'firstname':'Mark','lastname': 'Shuttleworth', 'submodel': {'age': 43}})

        # LIST MODEL: ALTER SUB MODEL
        model[0]['submodel'] = 43

        # LIST MODEL: DELETE SUB MODEL (SETS TO NULL on DB)
        del(model[0]['submodel'])

        # LIST MODEL: DELETE FIELD (SETS TO NULL on DB)
        del(model[0]['firstname'])
        if 'firstname' in model[0]:
            raise Exception('model __del__ method failed')

        # LIST MODEL: UPDATE FIELD
        model[0]['firstname'] = 'Bean'
        self.assertEqual(model[0]['firstname'].value(), 'Bean')

        # LIST MODEL: UPDATE SUB MODEL
        model[1]['submodel']['age'] = 83
        self.assertEqual(model[1]['submodel']['age'].value(), 83)

        # LIST MODEL: TEST ITERATOR
        for (i, row) in enumerate(model):
            if i == 0:
                self.assertEqual(row['firstname'].value(), 'Bean')
            if i == 1:
                self.assertEqual(row['firstname'].value(), 'Mark')
                self.assertEqual(row['submodel']['age'].value(), 83)
