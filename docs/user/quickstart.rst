.. _quickstart:

Quickstart
==========

If you haven't done so already, please refer to :ref:`install <install>` before continuing.

Your first Neutrino application
-------------------------------

Create a folder named after your project and use neutrino.py to setup clean initial project structure.

.. code:: bash

    $ mkdir project
    $ neutrino.py -c project

The following structure will be created:

**./settings.yaml** - Default Configuration file

**./myproject/** - Your Application - You can rename this or create multiples in the projects (just remember to update your settings.yaml modules)

**./myproject/__init__.py** - Loads your views and models.

**./myproject/views.py** - The Views for your project.

**./myproject/model.py** - Models for your project.

**./myproject/templates** - Jinja2 Templates specific to Application

**./myproject/static/myproject** - Static files for project. Images, stylesheets etc.

**./templates/** Global templates. Simply creating a template in here for example templates/myproject/test.html will override the application template.

**./static/** Your WSGI Webserver will serve these files. To populate or update them based on configured applications in settings.yaml run: neutrino.py -g .

**./tmp/** Temporary Folder for session data etc. To clear session data files that expired run neutrino.py -e . (Its recommended to run a cron a job hourly)

**./wsgi/** WSGI Scripts

**./wsgi/app.wsgi** WSGI Script for web server

Configuration for Apache2
~~~~~~~~~~~~~~~~~~~~~~~~~

You need to ensure that mod_wsgi is enabled and installed.
**The WSGI script is located within ./project/wsgi/app.wsgi**

Example of virtualhost::

    <VirtualHost *:80>
        ServerName myproject.org
        ServerAlias www.myproject.org

        ServerAdmin chris@fwiw.co.za
        DocumentRoot /var/www/project/static
        Alias /static /var/www/project/static

        ErrorLog ${APACHE_LOG_DIR}/project_error.log
        CustomLog ${APACHE_LOG_DIR}/project_access.log combined

        <Directory /var/www/project/static>
            Options Indexes FollowSymLinks
            AllowOverride None
            Require all granted
        </Directory>
        <Directory /var/www/project/wsgi>
            Options Indexes FollowSymLinks
            AllowOverride None
            Require all granted
        </Directory>

        WSGIScriptAlias / /var/www/project/wsgi/app.wsgi
        WSGIDaemonProcess blog user=www-data group=www-data processes=3 threads=10
        WSGIProcessGroup blog
    </VirtualHost>

WebApp by example
=================
The example will be creating a basic site with menu using bootstrap3

Bootstrap3 + Jquery
-------------------
You would require to place required files in your static directory for both Bootstrap and Jquery. However for this example we allow you to use our files. Keep in mind it will be faster to host these files yourself locally.

Create HTML Templates
---------------------
Neutrino uses Jinja2 Templating engine for generating templates.

Jinja2 Template Designer Documentation can be found here: http://jinja.pocoo.org/docs/dev/templates/

Create base.html inside your ./myproject/templates

.. code:: html

    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="http://neutrino.fwiw.co.za/static/myproject/bootstrap/css/bootstrap.css" />
            <script src="http://neutrino.fwiw.co.za/static/myproject/jquery-3.1.1.js"></script>
            <script src="http://neutrino.fwiw.co.za/static/myproject/bootstrap/js/bootstrap.js"></script>
            <title>My first neutrino application</title>
        </head>
        <body>

            <nav class="navbar navbar-inverse navbar-fixed-top">
                <div class="container">
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                            <span class="sr-only">Toggle navigation</span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                        </button>
                        <a class="navbar-brand" href="#">MyProject</a>
                    </div>
                    <div id="navbar" class="navbar-collapse collapse">
                        <ul class="nav navbar-nav navbar-left">
                            {{ MENU }}
                        </ul>
                    </div><!--/.navbar-collapse -->
                </div>
            </nav>

            <div class="jumbotron">
                <div class="container">
                    <h1>{{title}}</h1>
                    <p>{{description}}</p>
                </div>
            </div>

            {% block content %}{% endblock %}
        </body>
    </html>

Create page1.html inside your ./myproject/templates

.. code:: html

	{% extends "myproject/base.html" %}

	{% block content %}
	<div class="container">
		<H1>Hello world 1</H1>
	</div>
	{% endblock %}

Create page2.html inside your ./myproject/templates

.. code:: html

	{% extends "myproject/base.html" %}

	{% block content %}
	<div class="container">
		<H1>Hello world 2</H1>
	</div>
	{% endblock %}


Create Views
------------
Edit views.py and place inside your ./myproject/:

.. code:: python

    class Menu(nfw.Middleware):
        def pre(self, req, resp):
            menu = nfw.bootstrap3.Menu()
            menu.add_link('Page1',"%s/page1" % (req.app,))
            menu.add_link('Page2',"%s/page2" % (req.app,))
            nfw.jinja.globals['MENU'] = menu

    class MyWebsite(nfw.Resource):
        def __init__(self, app):
            app.router.add(nfw.HTTP_GET, '/', self.page1)
            app.router.add(nfw.HTTP_GET, '/page1', self.page1)
            app.router.add(nfw.HTTP_GET, '/page2', self.page2)

        def page1(self, req, resp):
            resp.headers['Content-Type'] = nfw.TEXT_HTML
            t = nfw.jinja.get_template('myproject/page1.html')
            title = "Example Title using template render"
            description = "Example Description using template render"
            resp.body = t.render(title=title, description=description)

        def page2(self, req, resp):
            resp.headers['Content-Type'] = nfw.TEXT_HTML
            t = nfw.jinja.get_template('myproject/page2.html')
            title = "Example Title using template render"
            description = "Example Description using template render"
            resp.body = t.render(title=title, description=description)

**Remember to add your middleware to the settings.yaml file**

.. code:: yaml

    application:
        name: "Project Name"
        modules: [ myproject ]
        middleware: [ myproject.Menu ]
        static: /static/
        session_timeout: 7200
        use_x_forwarded_host: false
        use_x_forwarded_port: false

RestAPI by example
==================

.. code:: python

	class BooksAPI(nfw.Resource):
		def __init__(self, app):
			app.router.add(nfw.HTTP_GET, '/', self.index)
			app.router.add(nfw.HTTP_POST, '/login', self.login)
			app.router.add(nfw.HTTP_GET, '/{id}', self.get)
			app.router.add(nfw.HTTP_DELETE, '/{id}', self.delete)
			app.router.add(nfw.HTTP_POST, '/', self.post)

		def index(self req, resp):
			resp.headers['Content-Type'] = nfw.APPLICATION_JSON
			resp.body = json.dumps(book_index())

		def get(self, req, resp, id):
			resp.headers['Content-Type'] = nfw.APPLICATION_JSON
			resp.body = json.dumps(book_view(id))

		def post(self, req, resp):
			resp.headers['Content-Type'] = nfw.APPLICATION_JSON
			resp.body = json.dumps(new_book(req.read()))

		def delete(self, req, resp, id):
			resp.headers['Content-Type'] = nfw.APPLICATION_JSON

			resp.body = json.dumps(delete_book(id))


Restarting
==========
When you have updated your application its neccesary to gracefully restart the web server. Otherwise you will still be running the old application and not see any of the updates.

