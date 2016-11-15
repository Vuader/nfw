.. Neutrino Framework documentation master file, created by
   sphinx-quickstart on Thu Nov 10 09:15:49 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The Neutrino Framework Documentation
====================================

Release v\ |version| (:ref:`Installation <install>`)

Neutrino is a flexible Python Web and RestApi application framework for rapid development. It's free and open source and before you ask: It's BSD Licensed! Contributions and contributors are welcome!

.. code:: python

    class Books(nfw.Resource):
        def __init__(self, app):
            app.router.add(nfw.HTTP_GET, '/books/{id}', self.view_book)

        def view_book(self, req, resp, id):
            resp.headers['Content-Type'] = nfw.TEXT_HTML
            title, book = book(id)
            t = nfw.jinja.get_template('myproject/view_book.html')
            resp.body = t.render(title=title, book=book)

Features
--------

- Routes based on URI templates.
- Ninja2 templating integration.
- Simple ORM. (serialized data json import and export)
- Mariadb/Mysql Pool manager and simple interface
- Policy/Rules Engine - Access control to resources.
- Logging Facilities.
- Loading of resource classes via configuration file.

Useful Links
------------

- `Neutrino Home <http://neutrino.fwiw.co.za/>`_
- `Neutrino @ PyPI <http://tbd>`_
- `Neutrino @ GitHub <http://github.com/vision1983/github/>`_

Documentation
-------------

.. toctree::
   :maxdepth: 2

   user/index
   api/index
   community/index
