.. _respreq:

Request and Response
====================
Each view in receives a request object that can be used to read the headers, query paramters and body of the request. The view also receives a response object that can be used for setting the status code, headers, and body of the response.

Request Object
--------------
The request object behaves like a IO file/object. You can use **.read()** and **.readline()** to read the raw request body. However POST data is also included in the request body and can be access via **.post**

**.post** is dictionary like object that returns keys within cgi.FieldStorage object. *You cannot use this method if you already read the body with another method* Example .post['id'].value

**.content_length** The length of the request body.

**.query** Dictionary like object of *urlparse.parse_qs()*. It contains the url query string values. Example *.query.get('id') / .query['id']*

**.headers** Dictionary like object that contains the request headers.

**.policy** Policy object used for validation.

**.view** the name of the route added.

**.method** the request method (GET,PUT,POST,DELETE etc)

**.environ** WSGI Environment object.

**.get_host()** Returns the originating host of the request using information from the *HTTP_X_FORWARDED_HOST* (if USE_X_FORWARDED_HOST is enabled) and HTTP_HOST headers, in that order. If they don’t provide a value, the method uses a combination of SERVER_NAME and SERVER_PORT as detailed in PEP 3333.

**.get_port()** Returns the originating port of the request using information from the *HTTP_X_FORWARDED_PORT*

**.get_proto()** return the web server protocol (HTTP/HTTPS)

**.get_script()** return the application url used in the WSGIScriptAlias for example.

**.get_full_path()** Returns the path, plus an appended query string, if applicable.

**.get_app_url()** Returns full url to access web application

**.get_absolute_url()** Returns the absolute URI form of location.

**.is_secure()** Returns *True* if the request is secure; that is, if it was made with HTTPS.

**.is_ajax()** Returns *True* if the request was made via an *XMLHttpRequest*, by checking the *HTTP_X_REQUESTED_WITH* header for the string '*XMLHttpRequest*'. Most modern JavaScript libraries send this header. If you write your own XMLHttpRequest call (on the browser side), you’ll have to set this header manually if you want *is_ajax()* to work.

**.is_mobile()** Returns *True* if HTTP_USER_AGENT matches Iphone or Anroid for example.

**.is_bot()** Returns *True* if HTTP_USER_AGENT matches Google Search or MSN/Bing for example.

Response Object
---------------
The response object behaves like a IO file/object. You can use **.write()** write to the response body. By setting a string value to the **.body** it will override anything from **.write()** method.

**.headers** Dictionary like object that is used to set headers.


