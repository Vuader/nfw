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
import os
import sys
import site
import re
import argparse
import logging
import time
import datetime
import hashlib
from wsgiref import simple_server

from pkg_resources import resource_stream
from pkg_resources import resource_listdir
from pkg_resources import resource_isdir
from pkg_resources import resource_exists

import nfw

log = logging.getLogger(__name__)


def _create_dir(path, new):
    new = os.path.normpath("%s%s" % (path, new))
    if not os.path.exists("%s" % (new,)):
        os.makedirs("%s" % (new,))
        print "Created %s" % (new,)


def _copy_resource(path, src, dst=''):
    dst = os.path.normpath("%s/%s/%s" % (path, dst, src))
    src_file = resource_stream('nfw', "resources/%s" % (src,)).read()
    if not os.path.exists(dst):
        with open("%s" % (dst,), 'wb') as handle:
            handle.write(src_file)
            print "Created %s" % (dst,)


def _copy_file(module, path, src, dst):
    try:
        nfw.utils.import_module(module)
    except ImportError:
        print "Neutrino python package not found %s" % (module,)
        exit()

    dst = os.path.normpath("%s/%s" % (path, dst))
    if resource_exists(module, src):
        src_file = resource_stream(module, src).read()
        if not os.path.exists(dst):
            with open("%s" % (dst,), 'wb') as handle:
                handle.write(src_file)
                print "Created %s" % (dst,)
        else:
            src_sig = hashlib.md5(src_file)
            dst_file = open(dst, 'rb').read()
            dst_sig = hashlib.md5(dst_file)
            if src_sig.hexdigest() != dst_sig.hexdigest():
                with open("%s" % (dst,), 'wb') as handle:
                    handle.write(src_file)
                    print "Updated %s" % (dst,)


def _empty_file(path, src, dst=''):
    dst = os.path.normpath("%s/%s/%s" % (path, dst, src))
    if not os.path.exists("%s" % (dst,)):
        with open("%s" % (dst,), 'wb') as handle:
            handle.write('')
            print "Created %s" % (dst,)


def static(args):
    path = os.path.abspath(args.path)
    app_root = path
    os.chdir(app_root)
    sys.path.append(app_root)
    site.addsitedir(app_root)

    def _walk(local, module, path):
        for filename in resource_listdir(module, path):
            fullname = path + '/' + filename
            if resource_isdir(module, fullname):
                _create_dir(local, "/%s" % (fullname,))
                _walk(local, module, fullname)
            else:
                _copy_file(module, local, fullname, fullname)

    if os.path.exists("%s/settings.cfg" % (path,)):
        config = nfw.Config("%s/settings.cfg" % (path,))
        app_config = config.get('application')
        modules = app_config.getitems('modules')
        for module in modules:
            if resource_exists(module, "static"):
                _create_dir('', "%s/static" % (path,))
                _walk(path, module, "static")


def setup(args):
    path = os.path.abspath(args.path)
    module = args.s
    _copy_file(module, path, 'resources/settings.cfg', 'settings.cfg')
    _copy_file(module, path, 'resources/policy.json', 'policy.json')
    _create_dir(path, '/wsgi')
    _copy_resource(path, '/wsgi/app.wsgi')
    _create_dir(path, '/templates')
    static(args)
    _create_dir(path, '/tmp')
    _create_dir(path, '/tmp/.cache')
    _create_dir(path, '/tmp/.cache/Python-Eggs')
    print "\nPlease ensure %s/tmp and sub-directories" % (path,) \
          + " is writeable by Web Server User\n"


def server(args):
    path = os.path.abspath(args.path)
    print "Loading Application %s" % (path,)
    ip = args.i
    port = args.p

    app_root = path
    os.chdir(app_root)
    sys.path.append(app_root)
    site.addsitedir(app_root)
    config = (os.path.abspath(os.path.join(path,
                              'settings.cfg')))
    os.environ['NEUTRINO_CONFIG'] = str(config)
    nfw_wsgi = nfw.Wsgi()

    httpd = simple_server.make_server('127.0.0.1',
                                       8000,
                                       nfw_wsgi.application())
    print "Running...\n"
    httpd.serve_forever()


def create(args):
    path = args.path
    if os.path.exists(path):
        _copy_resource(path, '/settings.cfg')
        _create_dir(path, '/wsgi')
        _copy_resource(path, '/wsgi/app.wsgi')
        _create_dir(path, '/templates')
        _create_dir(path, '/static')
        _create_dir(path, '/myproject')
        _copy_resource(path, '/myproject/__init__.py')
        _copy_resource(path, '/myproject/views.py')
        _empty_file(path, '/myproject/model.py')
        _create_dir(path, '/myproject/static')
        _create_dir(path, '/myproject/static/myproject')
        _create_dir(path, '/myproject/templates')
        _create_dir(path, '/tmp')
        _create_dir(path, '/tmp/.cache')
        _create_dir(path, '/tmp/.cache/Python-Eggs')
        print "\nPlease ensure %s/tmp and sub-directories" % (path,) \
              + " is writeable by Web Server User\n"
    else:
        print("Invalid path")


def session(args):
    path = args.path
    c = 0
    if os.path.exists("%s/settings.cfg" % (path,)):
        config = nfw.Config("%s/settings.cfg" % (path,))
        app_config = config.get('application', {})
        session_expire = app_config.get('session_expire', 3600)
        r = re.compile('^.*session$')
        if os.path.exists("%s/tmp" % (path,)):
            files = os.listdir("%s/tmp" % (path,))
            for f in files:
                fpath = "%s/tmp/%s" % (path, f)
                if os.path.isfile(fpath):
                    if r.match(fpath):
                        now = datetime.datetime.now()
                        ts = int(time.mktime(now.timetuple()))
                        stat = os.stat(fpath)
                        lm = int(stat.st_mtime)
                        if ts - lm > session_expire:
                            os.remove(fpath)
                            c += 1
            print "Removed expired sessions: %s\n" % (c,)
        else:
            print("Missing tmp folder")
    else:
        print("Missing settings.cfg or invalid path")


def main():
    description = "Neutrino Framework Applications Utility %s" % (nfw.version,)
    parser = argparse.ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('path', help='Application root path')
    group.add_argument('-c',
                       help='Create new application root structure',
                       dest='funcs',
                       const=create,
                       action='append_const')
    group.add_argument('-e',
                       help='Wipe expired sessions',
                       dest='funcs',
                       const=session,
                       action='append_const')
    group.add_argument('-s', help='Re-Initilize/Setup Application')
    group.add_argument('-g',
                       help='Collect and Populate /static' +
                            ' as per settings.cfg modules',
                       dest='funcs',
                       const=static,
                       action='append_const')
    group.add_argument('-t',
                       help='Start builtin server (only for testing)',
                       dest='funcs',
                       const=server,
                       action='append_const')
    parser.add_argument('-i', help='Binding IP Address (127.0.0.1)',
                        default='127.0.0.1')
    parser.add_argument('-p', help='Binding Port (8080)', default='8080')
    args = parser.parse_args()
    if args.funcs is not None:
        print "%s\n" % (description,)
        for f in args.funcs:
            f(args)
    if args.funcs is None or len(args.funcs) == 0:
        if args.s is not None:
            print "%s\n" % (description,)
            setup(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
