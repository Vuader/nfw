.. _settings:

settings.cfg
============

The settings.cfg file is located within your project directory. The purpose of this file to specify specific properties for the projects environment and import middleware and modules.

**Example:**

.. code::

    [application]
    name = Blog
    modules = pyblog, ipcalc
    middleware = pyblog.Login, pyblog.Globals
    static = /static
    session_timeout = 7200
    use_x_forwarded_host = false
    use_x_forwarded_port = false

    [mysql]
    database = blogdev
    host = 127.0.0.1
    username = blog
    password = t0ps3cret

    [redis]
    server = localhost
    port = 6379
    db = 0

    [logging]
    host = 127.0.0.1
    port = 514
    debug = true


