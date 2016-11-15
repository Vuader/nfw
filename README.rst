Neutrino
========
Project Status: Development

Neutrino is a flexible Python Web and RestApi application framework for rapid development. It's free and open source and before you ask: It's BSD Licensed! Contributions and contributors are welcome!

Quick Links
-----------

* `Website <http://neutrino.fwiw.co.za>`__.
* `Documentation <http://neutrino.fwiw.co.za/static/docs>`__.
* `Join mailing list <http://neutrino.fwiw.co.za/cgi-bin/mailman/listinfo/neutrino>`__.
* `Mail List Archives <http://neutrino.fwiw.co.za/pipermail/neutrino/>`__.

Installation
------------

Neutrino currently fully supports `CPython <https://www.python.org/downloads/>`__ 2.7.

A package is availible on PyPI for the Neutrino framework.
Installing it is as simple as:

.. code:: bash

    $ pip install nfw

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
