.. _views:

Views
=====

A view method, or *'view'* for short, is simply a Python class method that takes a web request and returns web response. The response can be the HTML content of a web page, json for restapi, image or anything else. The view contains the the logic neccessary to return that response. You can place your views anywhere, as long as its imported in the application __init__.py. The convention is to put the views in a file called views.py, placed in the the application directory.

*Views are placed in a class to group them and provide more flexibility.*

A simple view
-------------
Here's a view that returns the current date and time, as an HTML Document.

.. code:: python

    import datetime

    import nfw

    class MyViews(nfw.Resource):
        def __init__(self, app):
            app.router.add(nfw.HTTP_GET, '/', self.datetime)

        def datetime(self, req, resp):
            now = datetime.datetime.now()
            resp.body = "<html><body>It is now %s.</body></html>" % now
