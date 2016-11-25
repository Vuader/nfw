.. _templating:

Templating Engine
=================

Neutrino uses Jinja2 for a conveniant way to generate HTML dynamically. Most common approaches relies on templates. Templates contain the static parts of HTML output as well as some special syntax for inserting dynamic content.

There is a standard API for loading and rendering templates. Templates are located within your applications template directory. All the applications are actually a python package with __init__.py.

The root folder for your project contains a template directory used to override templates within packages.

Template Usage
--------------

If your applications name is 'myproject' and your template you wish to render is 'home.html' it would go something like this:

.. code:: python

    t = nfw.jinja.get_template('myproject/home.html')


**If you create a directory 'myproject' in the root folders template directory and place 'home.html' in there it will override the tempate within the package.**

To render the loaded template with some variables, just call the render() method on the template


.. code:: python

    resp.body = t.render(the='variables', go='here')

Unicode only
------------

Jinja2 is using Unicode internally which means that you have to pass Unicode objects to the render function or bytestrings that only consist of ASCII characters. Additionally newlines are normalized to one end of line sequence which is per default UNIX style (\n).

Python 2.x supports two ways of representing string objects. One is the str type and the other is the unicode type, both of which extend a type called basestring. Unfortunately the default is str which should not be used to store text based information unless only ASCII characters are used. With Python 2.6 it is possible to make unicode the default on a per module level and with Python 3 it will be the default.

To explicitly use a Unicode string you have to prefix the string literal with a u: u'Test'. That way Python will store the string as Unicode by decoding the string with the character encoding from the current Python module. If no encoding is specified this defaults to ‘ASCII’ which means that you can’t use any non ASCII identifier.

To set a better module encoding add the following comment to the first or second line of the Python module using the Unicode literal:

.. code:: python

	# -*- coding: utf-8 -*-

We recommend utf-8 as Encoding for Python modules and templates as it’s possible to represent every Unicode character in utf-8 and because it’s backwards compatible to ASCII. For Jinja2 the default encoding of templates is assumed to be utf-8.

Template Design
---------------

Jinja2 Template Designer Documentation can be found here: http://jinja.pocoo.org/docs/dev/templates/

