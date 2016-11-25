.. _model:

Model ORM
=========

A model is object with definitive information about your data. It contains the essentials field defined and behaviours of the data. Each model could map to a single database table. Its not neccesary to use database for the model.

The basics::

* Place models in your application model.py module
* Each model is a Python class that subclasses either nfw.Model or nfw.ModelDict.
* nfw.Model is used to represent a database table with rows for example.
* nfw.ModelDict is used to represent a single row within a database for example.
* Each attribute defined in the model class represents a database field.
* Meta class within the model class defines additional configuration.

Quick Example
-------------
The example defines a Person:

.. code:: python

    class Person(nfw.ModelDict):
        firstname = nfw.Model.Text(required=True, max_length=30)
        surname = nfw.Model.Text(required=True, max_length=30)
        age = nfw.Model.Integer(required=True, maximum=100)

The above Person model could use a database table like this:

.. code::

    CREATE TABLE person (
        "firstname" varchar(30) NOT NULL,
        "surname" varchar(30) NOT NULL,
        "age" int NOT NULL
    );

Some technical notes:

* The name of table is derived by the class name. However it can be overridden in the Meta class.
* The default primary key id is `id` unless specified otherwise in the Meta class.
* Using model in Neutrino only supports Mysql/MariaDb

Using models:

.. code:: python

    db = nfw.Mysql()
    model = Person(db=db)
    model.query()
    for row in model:
        print(row['firstname'])
    row.append({'firstname': 'New', 'surname': 'Guy'})
    model.commit()
