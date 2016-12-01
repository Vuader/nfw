.. _logging:

Logging
=======

Neutrino uses Python’s builtin logging module to perform system logging. The usage of this module is discussed in detail in Python’s own documentation.

.. code:: python

    import logging
    log = logging.getLogger(__name__)

    log.debug('This is a debug message')
    log.info('This is a informational message')
    log.warning('This is a warning message')
    log.error('This is a error message')
    log.critical('This is a critical message')

By default all debug messages are surpressed until you enable debug messages in your project settings.cfg

Settings Yaml Configuration

.. code::

    [logging]
    host = 127.0.0.1
    port = 514
    debug = true
