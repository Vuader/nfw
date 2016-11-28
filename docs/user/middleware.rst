.. _middleware:

Middleware
==========

Middleware components provide a way to execute logic before the framework routes each request, after each request is routed but before the response. Middleware is registered by the settings.yaml file. You need to ensure you import your application then you can specify middleware classes to be loaded located in the application views.py

The middleware is executed within the order defined in the settings.yaml configuration.

There are two methods you can can define for middleware *'pre'* and *'post'*. *'pre'* being before the request is routed and *'post'* being after.

Middleware Example Component

.. code:: python

    class Login(nfw.Middleware):
        def pre(self, req, resp):
            pass

    class Counter(nfw.Middleware):
        def post(self, req, resp):
            pass

