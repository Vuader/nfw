.. _install:

Installation
============

Neutrino currently fully supports `CPython <https://www.python.org/downloads/>`__ 2.7.

A package is availible on PyPI for the Neutrino framework.
Installing it is as simple as:

.. code:: bash

    $ pip install nfw

Dependencies
------------
Neutrino depends on:

.. include:: ../../requirements.txt

Ubuntu Notes
~~~~~~~~~~~~
Before running pip install nfw you may be required to install some distribution packages required.

.. code:: bash

    $ apt-get install libffi-dev
    $ apt-get install libmysqlclient-dev

WSGI Server
-----------
Neutrino speaks WSGI, and so in order to serve a Neutrino application, you will need a WSGI Server. Tested working with apache2 and mod_wsgi.

On Ubuntu the package is known as: libapache2-mod-wsgi

**Please note libapache2-mod-wsgi-py3 is for Python 3 and we only support 2.7 at this time.**


Source Code
-----------
Neutrino infrastructure and code is hosted on `GitHub <https://github.com/vision1983/nfw>`_. Making the code easy to browse, download, fork, etc. Pull requests are always welcome!

Clone the project like this:

.. code:: bash

	$ git clone https://github.com/vision1983/nfw.git

Once you have cloned the repo or downloaded a tarball from GitHub, you
can install Neutrino like this:

.. code:: bash

    $ cd nfw
    $ pip install .

Or, if you want to edit the code, first fork the main repo, clone the fork
to your desktop, and then run the following to install it using symbolic
linking, so that when you change your code, the changes will be automagically
available to your app without having to reinstall the package:

.. code:: bash

    $ cd nfw
    $ pip install -e .

You can manually test changes to the Neutrino framework by switching to the
directory of the cloned repo:

.. code:: bash

    $ cd nfw/tests
    $ python test.py

