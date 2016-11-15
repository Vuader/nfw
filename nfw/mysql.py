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
import thread
from Queue import Queue
import MySQLdb
import MySQLdb.cursors
import nfw

log = logging.getLogger(__name__)


class Mysql(object):
    _pool = {}
    _credentials = {}
    _thread = {}

    def __init__(self, name=None, host=None, username=None,
                 password=None, database=None):

        self.thread_id = thread.get_ident()

        if name is not None:
            self.name = name
        else:
            self.name = 'default'

        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.initialize()

    def initialize(self):
        if self.name not in self._pool:
            self._pool[self.name] = Queue(maxsize=0)

        if self.name not in self._credentials:
            self._credentials[self.name] = {}
        if self.host is not None:
            self._credentials[self.name]['host'] = self.host
        if self.username is not None:
            self._credentials[self.name]['username'] = self.username
        if self.password is not None:
            self._credentials[self.name]['password'] = self.password
        if self.database is not None:
            self._credentials[self.name]['database'] = self.database

        self.host = self._credentials[self.name].get('host','127.0.0.1')
        self.username = self._credentials[self.name].get('username','')
        self.password = self._credentials[self.name].get('password','')
        self.database = self._credentials[self.name].get('database','')

        if (self.thread_id in self._thread and
                self.name in self._thread[self.thread_id]):
            pass
        else:
            if self.thread_id not in self._thread:
                self._thread[self.thread_id] = {}
            if self._pool[self.name].empty():
                conn = connect(self.host,
                               self.username,
                               self.password,
                               self.database)
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            else:
                conn = self._pool[self.name].get(True)
                conn.ping(True)
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            self._thread[self.thread_id][self.name] = {}
            self._thread[self.thread_id][self.name]['db'] = conn
            self._thread[self.thread_id][self.name]['cursor'] = cursor
            self._thread[self.thread_id][self.name]['uncommited'] = False

    @staticmethod
    def close_all():
        thread_id = thread.get_ident()
        if thread_id in nfw.Mysql._thread:
            for o in nfw.Mysql._thread[thread_id]:
                db = nfw.Mysql._thread[thread_id][o]['db']
                cursor = nfw.Mysql._thread[thread_id][o]['cursor']
                uncommited = nfw.Mysql._thread[thread_id][o]['uncommited']
                if uncommited is True:
                    rollback(db)
                # Autocommit neccessary for next request to start new transactions.
                # If not applied select queries will return cached results
                commit(db)
                nfw.Mysql._pool[o].put_nowait(db)
            del nfw.Mysql._thread[thread_id]

    def close(self):
        if (self.thread_id in self._thread and
                self.name in self._thread[self.thread_id]):
            db = self._thread[self.thread_id][self.name]['db']
            cursor = self._thread[self.thread_id][self.name]['cursor']
            uncommited = self._thread[self.thread_id][self.name]['uncommited']
            if uncommited is True:
                rollback(db)
            self._pool[self.name].put_nowait(db)
            del self._thread[self.thread_id][self.name]

    def last_row_id(self):
        cursor = self._thread[self.thread_id][self.name]['cursor']
        return cursor.lastrowid

    def last_row_count(self):
        cursor = self._thread[self.thread_id][self.name]['cursor']
        return cursor.rowcount

    def execute(self, query=None, params=None):
        cursor = self._thread[self.thread_id][self.name]['cursor']
        result = execute(cursor, query, params)
        if len(query) > 6:
            if query[0:6].lower() != "select":
                self._thread[self.thread_id][self.name]['uncommited'] = True
        return result

    def commit(self):
        db = self._thread[self.thread_id][self.name]['db']
        commit(db)
        self._thread[self.thread_id][self.name]['uncommited'] = False

    def rollback(self):
        db = self._thread[self.thread_id][self.name]['db']
        rollback(db)
        self._thread[self.thread_id][self.name]['uncommited'] = False


def _log_query(query=None, params=None):
    try:
        if isinstance(params, tuple):
            log_query = query % params
        elif isinstance(params, list):
            log_query = query % tuple(params)
        else:
            log_query = query
    except Exception as e:
        log_query = query

    return log_query


def connect(host, username, password, database):
    timer = nfw.utils.timer()
    log.debug("Connecting Database Connection" +
              " (server=%s,username=%s,database=%s)" %
              (host, username,
               database))
    conn = MySQLdb.connect(host=host,
                           user=username,
                           passwd=password,
                           db=database,
                           use_unicode=True,
                           charset='utf8',
                           autocommit=False)
    timer = nfw.utils.timer(timer)
    log.debug("Connected Database Connection" +
              " (server=%s,username=%s,database=%s,%s,%s,%s)" %
              (host,
               username,
               database,
               conn.get_server_info(),
               conn.get_host_info(),
               conn.thread_id) +
              " (DURATION: %s)" % (timer))
    return conn


def execute(cursor, query=None, params=None):
    timer = nfw.utils.timer()

    log_query = _log_query(query, params)

    cursor.execute(query, params)
    result = cursor.fetchall()

    timer = nfw.utils.timer(timer)
    if timer > 0.1:
        log.debug("SQL !SLOW! Query %s (DURATION: %s)" % (log_query, timer))
    else:
        log.debug("SQL Query %s (DURATION: %s)" % (log_query, timer))

    return result


def commit(db):
    timer = nfw.utils.timer()
    db.commit()
    timer = nfw.utils.timer(timer)
    if timer > 0.1:
        log.debug("SQL !SLOW! Commit" +
                  " (%s,%s,%s) (DURATION: %s)" %
                  (db.get_server_info(),
                   db.get_host_info(),
                   db.thread_id,
                   timer))
    else:
        log.debug("SQL Commit" +
                  "(%s,%s,%s) (DURATION: %s)" %
                  (db.get_server_info(),
                   db.get_host_info(),
                   db.thread_id,
                   timer))


def rollback(db):
    timer = nfw.utils.timer()
    db.rollback()
    timer = nfw.utils.timer(timer)
    if timer > 0.1:
        log.debug("SQL !SLOW! Rollback" +
                  " (%s,%s,%s) (DURATION: %s)" %
                  (db.get_server_info(),
                   db.get_host_info(),
                   db.thread_id,
                   timer))
    else:
        log.debug("SQL Rollback" +
                  " (%s,%s,%s) (DURATION: %s)" %
                  (db.get_server_info(),
                   db.get_host_info(),
                   db.thread_id,
                   timer))
