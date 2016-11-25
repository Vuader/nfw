.. _policy:

Policy Engine
=============

Each Neutrino application has its own role-based access policies. They determine which user can access which resource objects in which way, and are defined in the service's policy.json file in the project root.

Whenever a request to Neutrino application is made, the service's policy engine uses the approriate policy definitions to determine if the call can be accepted. Any changes to policy.json are effective once the application is restarted.

A policy.json file is a text file in JSON (Javascript Object Notation) format. Each policy is defined by a one-line statement in the form "<target>" : "<rule>".

The target being the name of the URI added in the router. Example:

.. code:: python

    class Email(nfw.Resource):
        def __init__(self, app):
            app.router.add(nfw.HTTP_GET, '/email', self.sitemap, 'EMAIL:LIST')
            app.router.add(nfw.HTTP_GET, '/email/{id}', self.sitemap, 'EMAIL:EDIT')
            app.router.add(nfw.HTTP_PUT, '/email/{id}', self.sitemap, 'EMAIL:EDIT')
            app.router.add(nfw.HTTP_POST, '/email', self.sitemap, 'EMAIL:CREATE')
            app.router.add(nfw.HTTP_DELETE, '/delete/{id}', self.sitemap, 'EMAIL_DELETE')

The policy rule determines under which circumstances the requests is permitted. Usually this involves the user who makes the call for example.

4 Important objects for the request is accessible for comparison in policy.json::

 context (req.context) Temporary context data.
 session (req.session) Session data.
 kwargs URI Template variables
 qwargs (req.query) Query Strings in URI Request Data

All of the above are dictionaries, but accessible in object notiation. For example:

.. code:: json

    {
        "email:list": "$session.login:True",
        "email:edit": "$session.login:True and $context.admin:True",
        "email:create": "$session.login:True and $context.admin:True",
        "email:delete": "$session.login:True and $context.admin:True",
    }

Another more advanced example:

.. code:: json

    {
        "admin": "$session.login:True and ($context.admin:True or $context.role:Admins) ",
        "email:list": "$session.login:True",
        "email:edit": "$session.login:True and Rule:admin",
        "email:create": "$session.login:True and Rule:admin",
        "email:delete": "$session.login:True and Rule:admin",
    }

Syntax
------
A policy.json file consists of policies and aliases of the form target:rule or alias:definition, separated by commas and enclosed in curly braces:

.. code:: json

    {
       "alias 1" : "definition 1",
       "alias 2" : "definition 2",
       ...
       "target 1" : "rule 1",
       "target 2" : "rule 2",
       ....
    }

Aliases are simple single world `blah` while targets are defined as `name:subname`

Rules can be::

* always true. The action is always permitted. This can be written as "True".
* always false. The action is never permitted. Written as "False".
* a comparison of two values
* boolean expressions based on simpler rules
* <rule name>, the definition of an alias. (rules for aliases cannot contain ':')

Validating Rules
----------------
The policies are automatically enforced when the request is being processed. However it would make sense to be able to test rules for generating a menu for example.

Use the following on the `request` object within your resource/view code:

.. code:: json

    if req.policy.validate('EMAIL:LIST') is True:
        pass
